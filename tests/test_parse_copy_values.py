import pytest

from src.pg_stage.obfuscator import Obfuscator


@pytest.mark.parametrize("table_name", ['table', 'schema.table'])
def test_parse_copy_values_with_delete_comment(obfuscator_object: Obfuscator, table_name: str):
    """
    Arrange: Строка копирования данных в таблицу, которую необходимо удалить
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: Флаг _is_delete активен
    """
    obfuscator_object._delete_tables.add(table_name)
    obfuscator_object._parse_line(
        line=f'COPY {table_name} (column_1, column_2) FROM stdin;',
    )
    assert obfuscator_object._is_delete  # nosec
    assert obfuscator_object._is_data  # nosec


@pytest.mark.parametrize("table_name", ['table', 'schema.table'])
def test_parse_copy_values_without_delete_comment(obfuscator_object: Obfuscator, table_name: str):
    """
    Arrange: Строка копирования данных в таблицу, которую необходимо удалить
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: Флаг _is_delete активен
    """
    obfuscator_object._parse_line(
        line=f'COPY {table_name} (column_1, column_2) FROM stdin;',
    )
    assert not obfuscator_object._is_delete  # nosec
    assert obfuscator_object._is_data  # nosec
