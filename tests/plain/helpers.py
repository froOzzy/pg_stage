"""Доступ к сценариям единого сохранённого plain-дампа."""

import re
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / 'fixtures'
DUMP = FIXTURES / 'postgres15.sql'
SECTION = re.compile(
    r'^--\n-- (?:Data for )?Name: (?P<name>.*); Type: (?P<type>.*); Schema: (?P<schema>.*); Owner: .*\n--\n',
    re.MULTILINE,
)


def schema_name(case: str, original: str = 'public') -> str:
    """Получить схему сценария; исходная непубличная схема добавляется после двойного подчёркивания."""
    return case.replace('-', '_') + (f'__{original}' if original != 'public' else '')


def qualified_table(case: str, table: str) -> str:
    """Преобразовать исходное имя таблицы в квалифицированное имя внутри сценария."""
    schema, _, name = qualified(table).rpartition('.')
    return f'{schema_name(case, schema)}.{name}'


def qualified(table: str) -> str:
    """Добавить public к имени без схемы; входные имена должны быть простыми SQL-идентификаторами."""
    return table if '.' in table else f'public.{table}'


class PlainDump:
    """Доступ к сценариям единственного PG15 snapshot без изменения SQL.

    Сценарии изолированы схемами; методы принимают явный идентификатор сценария,
    не имя тестовой функции. Негативные сценарии нельзя обфусцировать все вместе.
    """

    @staticmethod
    def table(case: str, table: str) -> str:
        """Вернуть фактическое имя таблицы для assertions выбранного сценария."""
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
        """Найти единственную SQL-строку с префиксом; неоднозначность вызывает AssertionError."""
        matches = [line for line in self.read(case).splitlines() if line.startswith(prefix)]
        assert len(matches) == 1, f'Expected exactly one statement: {prefix}'
        return matches[0]
