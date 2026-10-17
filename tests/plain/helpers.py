"""Чтение настоящих plain-дампов и выделение их COPY-данных для проверок."""

import io
import re
from contextlib import redirect_stdout
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / 'fixtures'
DUMP = FIXTURES / 'postgres15.sql'
SECTION = re.compile(
    r'^--\n-- (?:Data for )?Name: (?P<name>.*); Type: (?P<type>.*); Schema: (?P<schema>.*); Owner: .*\n--\n',
    re.MULTILINE,
)


def schema_name(case: str, original: str = 'public') -> str:
    return case.replace('-', '_') + (f'__{original}' if original != 'public' else '')


def qualified_table(case: str, table: str) -> str:
    schema, _, name = qualified(table).rpartition('.')
    return f'{schema_name(case, schema)}.{name}'


def qualified(table: str) -> str:
    return table if '.' in table else f'public.{table}'


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


class PlainDump:
    @staticmethod
    def table(case: str, table: str) -> str:
        return qualified_table(case, table)

    def read(self, case: str) -> str:
        """Выбрать исходные секции сценария, не переписывая ни одной SQL-строки."""
        sql = DUMP.read_text(encoding='utf-8')
        assert '-- Dumped by pg_dump version 15.' in sql
        schemas = {schema_name(case), schema_name(case, 'schema')}
        body, delimiter, footer = sql.partition('\n--\n-- PostgreSQL database dump complete\n--\n')
        assert delimiter, 'Missing pg_dump footer'
        sections = list(SECTION.finditer(body))
        assert sections, 'Missing pg_dump object sections'
        selected = []
        for index, section in enumerate(sections):
            if section['schema'] in schemas or (section['type'] == 'SCHEMA' and section['name'] in schemas):
                end = sections[index + 1].start() if index + 1 < len(sections) else len(body)
                selected.append(body[section.start() : end])
        assert selected, f'Missing scenario {case}'
        return body[: sections[0].start()] + ''.join(selected) + delimiter + footer

    def statement(self, case: str, prefix: str) -> str:
        matches = [line for line in self.read(case).splitlines() if line.startswith(prefix)]
        assert len(matches) == 1, f'Expected exactly one statement: {prefix}'
        return matches[0]
