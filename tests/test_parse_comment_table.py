import pytest

from src.pg_stage.obfuscators.plain import PlainObfuscator


@pytest.mark.parametrize('table_name', ['public.deleted_table', 'schema.deleted_table'])
def test_parse_comment_table_with_mutation(
    obfuscator_object: PlainObfuscator,
    table_name: str,
    plain_dump,
) -> None:
    """
    Arrange: Строка, в которой есть комментарий к таблице
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: Таблица добавлена в список _delete_tables
    """
    obfuscator_object._parse_line(
        line=plain_dump.statement('metadata', f'COMMENT ON TABLE {table_name} '),
    )
    assert table_name in obfuscator_object._delete_tables  # nosec


@pytest.mark.parametrize('table_name', ['public.kept_table', 'schema.kept_table'])
def test_parse_comment_table_with_invalid_mutation(
    obfuscator_object: PlainObfuscator,
    table_name: str,
    plain_dump,
) -> None:
    """
    Arrange: Строка, в которой есть невалидный комментарий к таблице
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: Мутация не добавлена в список _delete_tables
    """
    obfuscator_object._parse_line(
        line=plain_dump.statement('metadata', f'COMMENT ON TABLE {table_name} '),
    )
    assert table_name not in obfuscator_object._delete_tables  # nosec
