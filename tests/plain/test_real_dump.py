import pytest

from pg_stage.obfuscators.plain import PlainObfuscator
from tests.plain.helpers import copy_rows, obfuscate


def sql_structure(sql: str) -> list[str]:
    lines = []
    in_copy = False
    for line in sql.splitlines():
        if line.startswith('COPY '):
            in_copy = True
            lines.append(line)
        elif line == '\\.':
            in_copy = False
            lines.append(line)
        elif not in_copy:
            lines.append(line)
    return lines


@pytest.mark.parametrize(
    'case',
    [
        'test_equal_condition',
        'test_parse_copy_values_with_delete_tables',
        'test_parse_copy_values_with_relations',
        'test_obfuscate_uuid_by_source_value',
    ],
)
def test_real_dump_preserves_sql_structure(plain_dump, case: str) -> None:
    """
    Arrange: Исходные секции сценария из общего дампа PG15 с заголовком, DDL, комментариями и COPY
    Act: Обработка дампа через публичный PlainObfuscator.run
    Assert: Изменены только строки данных, весь SQL вне COPY и набор таблиц сохранены
    """
    original = plain_dump.read(case)
    result = obfuscate(PlainObfuscator(), original)
    assert sql_structure(result) == sql_structure(original)
    assert set(copy_rows(result)) == set(copy_rows(original))
