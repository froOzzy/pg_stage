import pytest

from src.pg_stage.obfuscator import Obfuscator


@pytest.mark.parametrize("table_name", ['table', 'schema.table'])
def test_parse_comment_table_with_mutation(obfuscator_object: Obfuscator, table_name: str):
    """
    Arrange: Строка, в которой есть комментарий к таблице
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: Таблица добавлена в список _delete_tables
    """
    obfuscator_object._parse_line(
        line=f'COMMENT ON TABLE {table_name}' + ' IS \'anon: {"mutation_name": "delete"}\';',
    )
    assert table_name in obfuscator_object._delete_tables  # nosec


@pytest.mark.parametrize("table_name", ['table', 'schema.table'])
def test_parse_comment_table_with_invalid_mutation(obfuscator_object: Obfuscator, table_name: str):
    """
    Arrange: Строка, в которой есть невалидный комментарий к таблице
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: Мутация не добавлена в список _delete_tables
    """
    obfuscator_object._parse_line(
        line=f'COMMENT ON TABLE {table_name}' + ' IS \'anon: {"mutation_name": "set"}\';',
    )
    assert table_name not in obfuscator_object._delete_tables  # nosec
