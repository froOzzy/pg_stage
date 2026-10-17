"""Чтение настоящих plain-дампов и выделение их COPY-данных для проверок."""

import io
from contextlib import redirect_stdout
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / 'fixtures'


def copy_rows(sql: str) -> dict[str, list[str]]:
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


def obfuscate(parser, sql: str) -> str:
    output = io.StringIO()
    with redirect_stdout(output):
        parser.run(stdin=io.StringIO(sql))
    return output.getvalue()


class PlainDumps:
    def __init__(self, major: int):
        self.major = major

    def read(self, case: str) -> str:
        sql = (FIXTURES / f'pg{self.major}' / f'{case}.sql').read_text(encoding='utf-8')
        assert f'-- Dumped by pg_dump version {self.major}.' in sql
        return sql

    def statement(self, case: str, prefix: str) -> str:
        matches = [line for line in self.read(case).splitlines() if line.startswith(prefix)]
        assert len(matches) == 1, f'Expected exactly one statement: {prefix}'
        return matches[0]
