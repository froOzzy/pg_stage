"""Общие проверки plain-SQL, полученного из текстовых и custom-дампов."""

import io
from contextlib import redirect_stdout

from pg_stage.obfuscators.plain import PlainObfuscator


def copy_rows(sql: str) -> dict[str, list[str]]:
    """Извлечь строки COPY без декодирования PostgreSQL escapes.

    Возвращает отображение квалифицированных имён в списки строк без перевода строки.
    Повторный COPY одной таблицы или незавершённый блок вызывают AssertionError.
    Поддерживается только COPY ... FROM stdin из наших pg_dump-фикстур.
    """
    tables = {}
    table = None
    for line in sql.splitlines():
        if line.startswith('COPY '):
            table = line.split()[1]
            assert table not in tables, f'Duplicate COPY for {table}'
            tables[table] = []
        elif line == '\\.':
            assert table is not None, 'Unexpected COPY terminator'
            table = None
        elif table is not None:
            tables[table].append(line)
    assert table is None, 'Unterminated COPY block'
    return tables


def obfuscate(parser: PlainObfuscator, sql: str) -> str:
    """Обработать SQL публичным run и вернуть перехваченный stdout.

    Переданный parser изменяет своё состояние; исключения обфускатора передаются тесту.
    Перехват stdout локален процессу, поэтому helper не предназначен для потоков.
    """
    output = io.StringIO()
    with redirect_stdout(output):
        parser.run(stdin=io.StringIO(sql))
    return output.getvalue()
