import pytest

from src.pg_stage.obfuscator import Obfuscator


@pytest.mark.parametrize("table_name, column_name", [('table', 'column'), ('schema.table', 'column')])
def test_parse_comment_column_with_mutation(
    obfuscator_object: Obfuscator,
    table_name: str,
    column_name: str,
):
    """
    Arrange: Строка, в которой есть комментарий к колонке
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: Мутация добавлена в список _map_tables
    """
    obfuscator_object._parse_line(
        line=f'COMMENT ON COLUMN {table_name}.{column_name}' + ' IS \'anon: [{"mutation_name": "null"}]\';',
    )
    assert table_name in obfuscator_object._map_tables  # nosec
    assert column_name in obfuscator_object._map_tables[table_name]  # nosec
    assert 'null' == obfuscator_object._map_tables[table_name][column_name][0]['mutation_name']  # nosec


@pytest.mark.parametrize("table_name, column_name", [('table', 'column'), ('schema.table', 'column')])
def test_parse_comment_column_without_mutation(
    obfuscator_object: Obfuscator,
    table_name: str,
    column_name: str,
):
    """
    Arrange: Строка, в которой есть комментарий к колонке с неизвестной мутацией
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: Вброшено исключение ValueError
    """
    with pytest.raises(ValueError):
        obfuscator_object._parse_line(
            line=f'COMMENT ON COLUMN {table_name}.{column_name}' + ' IS \'anon: [{"mutation_name": "not_found"}]\';',
        )


@pytest.mark.parametrize("table_name, column_name", [('table', 'column'), ('schema.table', 'column')])
def test_parse_comment_column_with_invalid_mutation(
    obfuscator_object: Obfuscator,
    table_name: str,
    column_name: str,
):
    """
    Arrange: Строка, в которой есть невалидный комментарий к колонке
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: Мутация не добавлена в список _map_tables
    """
    obfuscator_object._parse_line(
        line=f'COMMENT ON COLUMN {table_name}.{column_name}' + ' IS \'anon: {\'mutation_name": "null"}\';',
    )
    assert table_name not in obfuscator_object._map_tables  # nosec
