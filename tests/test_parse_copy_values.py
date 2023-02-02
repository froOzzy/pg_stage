import pytest

from src.pg_stage.obfuscator import Obfuscator


@pytest.fixture(autouse=True)
def obfuscator_object_with_delete_tables_by_pattern():
    return Obfuscator(delete_tables_by_pattern=[r'_table', r'schema\.\_table'])


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


@pytest.mark.parametrize("table_name", ['_table', 'schema._table'])
def test_parse_copy_values_without_delete_tables_by_pattern(
    obfuscator_object_with_delete_tables_by_pattern: Obfuscator,
    table_name: str,
):
    """
    Arrange: Строка копирования данных в таблицу, которую необходимо удалить исходя из параметра
    delete_tables_by_pattern
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: Флаг _is_delete активен
    """
    obfuscator_object_with_delete_tables_by_pattern._parse_line(
        line=f'COPY {table_name} (column_1, column_2) FROM stdin;',
    )
    assert obfuscator_object_with_delete_tables_by_pattern._is_delete  # nosec
    assert obfuscator_object_with_delete_tables_by_pattern._is_data  # nosec


@pytest.mark.parametrize("table_name", ['table', 'schema.table'])
def test_parse_copy_values_without_delete_tables_by_pattern_and_not_found_table(
    obfuscator_object_with_delete_tables_by_pattern: Obfuscator,
    table_name: str,
):
    """
    Arrange: Строка копирования данных в таблицу, которая не должна быть удалена, т.к. не входит в список
    delete_tables_by_pattern
    delete_tables_by_pattern
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: Флаг _is_delete не активен
    """
    obfuscator_object_with_delete_tables_by_pattern._parse_line(
        line=f'COPY {table_name} (column_1, column_2) FROM stdin;',
    )
    assert not obfuscator_object_with_delete_tables_by_pattern._is_delete  # nosec
    assert obfuscator_object_with_delete_tables_by_pattern._is_data  # nosec
