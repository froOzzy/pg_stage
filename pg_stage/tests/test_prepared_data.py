import pytest

from pg_stage.obfuscator import Obfuscator


@pytest.fixture(autouse=True)
def obfuscator_object():
    return Obfuscator()


def test_parse_copy_values_with_delete_table(obfuscator_object: Obfuscator):
    """
    Arrange: Дамп таблицы, данные которой необходимо удалить
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout нет данных из таблицы
    """
    with open('pg_stage/tests/sql/test_parse_copy_values_with_delete_tables.sql') as file:
        dump_sql = file.read()

    result = []
    for line in dump_sql.splitlines():
        new_line = obfuscator_object._parse_line(line=line)
        if new_line is not None:
            result.append(new_line)

    assert_result = [
        'COMMENT ON TABLE table_1 IS \'anon: {"mutation_name": "delete"}\';',
        'COPY table_1 (id, message, recipient, notes) FROM stdin;',
        '\\.',
        '',
        'COMMENT ON TABLE schema.table_2 IS \'anon: {"mutation_name": "delete"}\';',
        'COPY schema.table_2 (id, message, recipient, notes) FROM stdin;',
        '\\.',
    ]
    assert assert_result == result
