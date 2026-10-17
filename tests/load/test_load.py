"""Нагрузочные тесты запускаются явно: pytest tests/load --run-load."""

import json
import os
import subprocess
import sys
from statistics import median

import pytest

from tests.load import SCENARIOS
from tests.load.plugin import PROJECT_ROOT


@pytest.mark.load
@pytest.mark.parametrize('scenario', SCENARIOS)
@pytest.mark.parametrize('output_mode', ['discard', 'file'])
def test_plain_dump_under_load(request, load_results, scenario, output_mode):
    """
    Arrange: Потоковый синтетический дамп и отдельный процесс для каждого повторного замера
    Act: Обработка дампа с измерением времени, CPU, пиковой ОЗУ и дискового I/O
    Assert: Результат корректен, число строк сохранено, явно заданные пороги ресурсов соблюдены
    """
    config = request.config
    selected_mode = config.getoption('--load-output-mode')
    if selected_mode not in ('both', output_mode):
        pytest.skip(f'Output mode {output_mode} not selected')
    runs = []
    for repetition in range(config.getoption('--load-repeats')):
        command = [
            sys.executable,
            '-m',
            'tests.load.worker',
            '--scenario',
            scenario,
            '--rows',
            str(config.getoption('--load-rows')),
            '--output-mode',
            output_mode,
        ]
        if config.getoption('--load-tmp-dir'):
            command.extend(['--tmp-dir', config.getoption('--load-tmp-dir')])
        process = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=config.getoption('--load-timeout'),
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONHASHSEED': '0'},
        )
        assert process.returncode == 0, process.stderr
        result = json.loads(process.stdout)
        result['repetition'] = repetition + 1
        load_results.append(result)
        runs.append(result)
        assert result['rows'] == config.getoption('--load-rows') * (2 if scenario == 'relations' else 1)
        assert result['wall_seconds'] > 0
        assert result['input_bytes'] > 0 and result['output_bytes'] > 0
        if output_mode == 'discard':
            assert result['io']['write_bytes'] == 0, 'Unexpected storage writes in discard mode'

    min_speed = config.getoption('--load-min-rows-per-second')
    max_rss = config.getoption('--load-max-rss-mib')
    max_write = config.getoption('--load-max-write-mib')
    if min_speed is not None:
        assert median(run['rows_per_second'] for run in runs) >= min_speed, 'Throughput below configured limit'
    if max_rss is not None:
        assert max(run['peak_rss_mib'] for run in runs) <= max_rss, 'Peak RSS above configured limit'
    if max_write is not None:
        assert max(run['io']['write_bytes'] for run in runs) / 1024**2 <= max_write, (
            'Storage writes above configured limit'
        )
