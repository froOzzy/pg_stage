"""Изолированный замер потоковой обработки plain-дампа на Linux."""

import argparse
import hashlib
import json
import os
import random
import resource
import sys
import tempfile
import time
import uuid
from contextlib import redirect_stdout
from datetime import date
from typing import Any, BinaryIO, Iterator, Optional

from pg_stage.obfuscators.plain import PlainObfuscator
from tests.load import SCENARIOS


def proc_counters(path: str) -> dict[str, int]:
    """Прочитать целочисленные счётчики /proc; значения возвращаются в единицах ядра.

    Для /proc/self/io rchar/wchar/read_bytes/write_bytes измеряются в байтах,
    syscr/syscw — числом вызовов; это не процент занятости накопителя.
    """
    with open(path) as stream:
        return {key: int(value.split()[0]) for key, value in (line.split(':', 1) for line in stream)}


def memory_kib() -> dict[str, int]:
    """Вернуть текущий RSS и максимум RSS за жизнь процесса из /proc/self/status, в KiB."""
    values = {}
    with open('/proc/self/status') as stream:
        for line in stream:
            if line.startswith(('VmRSS:', 'VmHWM:')):
                values[line.split(':', 1)[0]] = int(line.split()[1])
    return values


class DumpInput:
    """Лениво генерируемый plain-поток без хранения всех строк в памяти.

    rows задаёт число строк на таблицу; relations содержит две таблицы.
    bytes учитывает фактически прочитанные UTF-8 байты, width — число колонок.
    """

    def __init__(self, scenario: str, rows: int) -> None:
        self.scenario = scenario
        self.rows = rows
        self.bytes = 0
        self.width = 100 if scenario == 'wide' else 6

    @staticmethod
    def comment(table: str, column: str, mutations: list[dict[str, Any]]) -> str:
        """Создать COMMENT с JSON-конфигурацией мутаций для синтетического дампа."""
        return f"COMMENT ON COLUMN {table}.{column} IS 'anon: {json.dumps(mutations)}';\n"

    def lines(self) -> Iterator[str]:
        """Выдать комментарии, COPY, строки и терминаторы выбранного сценария."""
        mutation = {'mutation_name': 'random_choice', 'mutation_kwargs': {'choices': ['hidden']}}
        if self.scenario == 'conditions':
            mutation['conditions'] = [{'column_name': 'c2', 'operation': 'equal', 'value': 'yes'}]
        elif self.scenario == 'json':
            mutation = {
                'mutation_name': 'json_update',
                'mutation_kwargs': {'mutations_by_key': {'secret': [mutation]}},
            }
        elif self.scenario == 'source_column':
            yield self.comment(
                'users',
                'c3',
                [
                    {
                        'mutation_name': 'uuid5_by_source_value',
                        'mutation_kwargs': {
                            'source_column': 'c1',
                            'namespace': '6ba7b810-9dad-11d1-80b4-00c04fd430c8',
                        },
                    }
                ],
            )

        tables = ('users', 'peers') if self.scenario == 'relations' else ('users',)
        for table in tables:
            if self.scenario == 'relations':
                mutation = {
                    'mutation_name': 'first_name',
                    'relations': [
                        {
                            'table_name': 'peers' if table == 'users' else 'users',
                            'column_name': 'c1',
                            'from_column_name': 'c0',
                            'to_column_name': 'c0',
                        }
                    ],
                }
            if self.scenario != 'passthrough':
                yield self.comment(table, 'c1', [mutation])
            yield f'COPY {table} ({", ".join(f"c{i}" for i in range(self.width))}) FROM stdin;\n'
            for index in range(self.rows):
                secret = '{"secret":"private","nested":{"secret":"private"}}' if self.scenario == 'json' else 'private'
                values = [str(index), secret, 'yes' if index % 2 == 0 else 'no', 'original', '\\N', 'text\\tvalue']
                if self.width > 6:
                    values.extend(['unchanged'] * (self.width - 6))
                yield '\t'.join(values) + '\n'
            yield '\\.\n'

    def __iter__(self) -> Iterator[str]:
        for line in self.lines():
            self.bytes += len(line.encode('utf-8'))
            yield line


class DumpOutput:
    """Приёмник stdout: счётчики, выборочная проверка и опциональная бинарная запись.

    Проверяются обе ветки conditions; для relations хешируются все строки обеих
    таблиц. stream=None отбрасывает вывод, сохраняя проверки и счётчики.
    """

    def __init__(self, workload: DumpInput, stream: Optional[BinaryIO]) -> None:
        self.workload = workload
        self.stream = stream
        self.bytes = 0
        self.rows = 0
        self.in_copy = False
        self.digest = hashlib.sha256()
        self.table_digests = []

    def write(self, text: str) -> int:
        """Принять строку stdout, проверить выборку и вернуть число принятых символов."""
        data = text.encode('utf-8')
        self.bytes += len(data)
        if self.stream is not None:
            self.stream.write(data)
        if text.startswith('COPY '):
            self.in_copy = True
        elif text == '\\.\n':
            self.in_copy = False
            self.table_digests.append(self.digest.hexdigest())
            self.digest = hashlib.sha256()
        elif self.in_copy:
            self.rows += 1
            if self.workload.scenario == 'relations':
                self.digest.update(data)
            if (self.rows - 1) % self.workload.rows % 1000 in (0, 1):
                self.validate_row(text.rstrip('\n').split('\t'))
        return len(text)

    def validate_row(self, values: list[str]) -> None:
        """Проверить мутации и неизменённые колонки; нарушение вызывает AssertionError."""
        if len(values) != self.workload.width or values[4:] != ['\\N', 'text\\tvalue'] + ['unchanged'] * (
            self.workload.width - 6
        ):
            message = 'Column order or unchanged values corrupted'
            raise AssertionError(message)
        scenario = self.workload.scenario
        if values[2] != ('yes' if int(values[0]) % 2 == 0 else 'no'):
            message = 'Unchanged condition column corrupted'
            raise AssertionError(message)
        if scenario != 'source_column' and values[3] != 'original':
            message = 'Unchanged column corrupted'
            raise AssertionError(message)
        if scenario in ('mutation', 'wide', 'source_column') and values[1] != 'hidden':
            message = 'Mutation was not applied'
            raise AssertionError(message)
        if scenario == 'passthrough' and values[1] != 'private':
            message = 'Passthrough data changed'
            raise AssertionError(message)
        if scenario == 'relations' and values[1] == 'private':
            message = 'Related value was not obfuscated'
            raise AssertionError(message)
        if scenario == 'conditions' and values[1] != ('hidden' if int(values[0]) % 2 == 0 else 'private'):
            message = 'Conditional mutation is incorrect'
            raise AssertionError(message)
        if scenario == 'json' and json.loads(values[1]) != {'secret': 'hidden', 'nested': {'secret': 'hidden'}}:
            message = 'JSON mutation is incorrect'
            raise AssertionError(message)
        if scenario == 'source_column' and values[3] != str(uuid.uuid5(uuid.NAMESPACE_DNS, f'hidden-{date.today()}')):
            message = 'Source column mutation is incorrect'
            raise AssertionError(message)


def measure(scenario: str, rows: int, output_mode: str, tmp_dir: Optional[str] = None) -> dict[str, Any]:
    """Измерить один сценарий в свежем Linux-процессе и вернуть словарь метрик.

    В wall/CPU входят генерация входа, обфускация и проверка вывода; в file также
    flush/fsync. Импорты и создание parser исключены из времени. RSS в MiB —
    максимум за жизнь процесса, а не дельта; baseline позволяет оценить его вклад.
    I/O и resource-счётчики — дельты замера. relations хранит O(rows) соответствий.
    Ошибки результата передаются вызывающему процессу и делают запуск неуспешным.
    """
    random.seed(42)
    parser = PlainObfuscator()
    workload = DumpInput(scenario, rows)
    # Файл создаётся до замера; его запись, flush и fsync входят в измерение.
    with tempfile.TemporaryFile(dir=tmp_dir) as output_file:
        output = DumpOutput(workload, output_file if output_mode == 'file' else None)
        baseline_memory = memory_kib()
        before_io = proc_counters('/proc/self/io')
        before_usage = resource.getrusage(resource.RUSAGE_SELF)
        started = time.perf_counter()
        with redirect_stdout(output):
            parser.run(stdin=workload)
        if output_mode == 'file':
            output_file.flush()
            os.fsync(output_file.fileno())
        elapsed = time.perf_counter() - started
        after_usage = resource.getrusage(resource.RUSAGE_SELF)
        after_io = proc_counters('/proc/self/io')
        final_memory = memory_kib()
        expected_rows = rows * (2 if scenario == 'relations' else 1)
        if output.rows != expected_rows:
            message = f'Expected {expected_rows} rows, got {output.rows}'
            raise AssertionError(message)
        if scenario == 'relations' and (
            len(output.table_digests) != 2 or output.table_digests[0] != output.table_digests[1]
        ):
            message = 'Related tables contain inconsistent values'
            raise AssertionError(message)
        cpu_user = after_usage.ru_utime - before_usage.ru_utime
        cpu_system = after_usage.ru_stime - before_usage.ru_stime
        return {
            'scenario': scenario,
            'rows_per_table': rows,
            'rows': output.rows,
            'output_mode': output_mode,
            'wall_seconds': elapsed,
            'rows_per_second': output.rows / elapsed,
            'input_bytes': workload.bytes,
            'output_bytes': output.bytes,
            'input_mib_per_second': workload.bytes / elapsed / 1024**2,
            'cpu_user_seconds': cpu_user,
            'cpu_system_seconds': cpu_system,
            'cpu_percent_one_core': (cpu_user + cpu_system) / elapsed * 100,
            'baseline_rss_mib': baseline_memory['VmRSS'] / 1024,
            'baseline_peak_rss_mib': baseline_memory['VmHWM'] / 1024,
            'peak_rss_mib': final_memory['VmHWM'] / 1024,
            'final_rss_mib': final_memory['VmRSS'] / 1024,
            'block_inputs': after_usage.ru_inblock - before_usage.ru_inblock,
            'block_outputs': after_usage.ru_oublock - before_usage.ru_oublock,
            'minor_faults': after_usage.ru_minflt - before_usage.ru_minflt,
            'major_faults': after_usage.ru_majflt - before_usage.ru_majflt,
            'voluntary_context_switches': after_usage.ru_nvcsw - before_usage.ru_nvcsw,
            'involuntary_context_switches': after_usage.ru_nivcsw - before_usage.ru_nivcsw,
            'io': {key: after_io[key] - before_io[key] for key in before_io},
        }


if __name__ == '__main__':
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--scenario', choices=SCENARIOS, required=True)
    args.add_argument('--rows', type=int, required=True)
    args.add_argument('--output-mode', choices=('discard', 'file'), required=True)
    args.add_argument('--tmp-dir', default=None)
    options = args.parse_args()
    json.dump(measure(options.scenario, options.rows, options.output_mode, options.tmp_dir), sys.stdout)
    sys.stdout.write('\n')
