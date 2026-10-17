from src.pg_stage.obfuscators.plain import PlainObfuscator
from tests.plain.helpers import copy_rows, obfuscate


def test_equal_condition(obfuscator_object: PlainObfuscator, plain_dump) -> None:
    """
    Arrange: Дамп таблиц, данные в которой необходимо обфусцировать
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout обфусцированы только те данные, условия которых выполняются
    """
    dump_sql = plain_dump.read('test_equal_condition')

    rows = copy_rows(obfuscate(obfuscator_object, dump_sql))['public.table_1']
    assert len(rows) == 2
    for new_line in rows:
        if new_line.startswith('1'):
            assert 'test@mail.ru' not in new_line  # nosec

        if new_line.startswith('2'):
            assert 'test@mail.ru' in new_line  # nosec


def test_not_equal_condition(obfuscator_object: PlainObfuscator, plain_dump) -> None:
    """
    Arrange: Дамп таблиц, данные в которой необходимо обфусцировать
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout обфусцированы только те данные, условия которых выполняются
    """
    dump_sql = plain_dump.read('test_not_equal_condition')

    rows = copy_rows(obfuscate(obfuscator_object, dump_sql))['public.table_1']
    assert len(rows) == 2
    for new_line in rows:
        if new_line.startswith('1'):
            assert 'test@mail.ru' in new_line  # nosec

        if new_line.startswith('2'):
            assert 'test@mail.ru' not in new_line  # nosec


def test_by_pattern_condition(obfuscator_object: PlainObfuscator, plain_dump) -> None:
    """
    Arrange: Дамп таблиц, данные в которой необходимо обфусцировать
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout обфусцированы только те данные, условия которых выполняются
    """
    dump_sql = plain_dump.read('test_by_pattern_condition')

    rows = copy_rows(obfuscate(obfuscator_object, dump_sql))['public.table_1']
    assert len(rows) == 2
    for new_line in rows:
        if new_line.startswith('1'):
            assert 'test@mail.ru' not in new_line  # nosec

        if new_line.startswith('2'):
            assert 'test@mail.ru' not in new_line  # nosec
