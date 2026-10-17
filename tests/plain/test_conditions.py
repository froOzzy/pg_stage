from pg_stage.obfuscators.plain import PlainObfuscator
from tests.helpers import copy_rows, obfuscate


def test_equal_condition(obfuscator_object: PlainObfuscator, plain_dump) -> None:
    """
    Arrange: Дамп таблиц, данные в которой необходимо обфусцировать
    Act: Обработка сценария через PlainObfuscator.run
    Assert: В stdout обфусцированы только те данные, условия которых выполняются
    """
    case = 'test_equal_condition'
    dump_sql = plain_dump.read(case)

    rows = copy_rows(obfuscate(obfuscator_object, dump_sql))[plain_dump.table(case, 'table_1')]
    assert len(rows) == 2
    for new_line in rows:
        if new_line.startswith('1'):
            assert 'test@mail.ru' not in new_line  # nosec

        if new_line.startswith('2'):
            assert 'test@mail.ru' in new_line  # nosec


def test_not_equal_condition(obfuscator_object: PlainObfuscator, plain_dump) -> None:
    """
    Arrange: Дамп таблиц, данные в которой необходимо обфусцировать
    Act: Обработка сценария через PlainObfuscator.run
    Assert: В stdout обфусцированы только те данные, условия которых выполняются
    """
    case = 'test_not_equal_condition'
    dump_sql = plain_dump.read(case)

    rows = copy_rows(obfuscate(obfuscator_object, dump_sql))[plain_dump.table(case, 'table_1')]
    assert len(rows) == 2
    for new_line in rows:
        if new_line.startswith('1'):
            assert 'test@mail.ru' in new_line  # nosec

        if new_line.startswith('2'):
            assert 'test@mail.ru' not in new_line  # nosec


def test_by_pattern_condition(obfuscator_object: PlainObfuscator, plain_dump) -> None:
    """
    Arrange: Дамп таблиц, данные в которой необходимо обфусцировать
    Act: Обработка сценария через PlainObfuscator.run
    Assert: В stdout обфусцированы только те данные, условия которых выполняются
    """
    case = 'test_by_pattern_condition'
    dump_sql = plain_dump.read(case)

    rows = copy_rows(obfuscate(obfuscator_object, dump_sql))[plain_dump.table(case, 'table_1')]
    assert len(rows) == 2
    for new_line in rows:
        if new_line.startswith('1'):
            assert 'test@mail.ru' not in new_line  # nosec

        if new_line.startswith('2'):
            assert 'test@mail.ru' not in new_line  # nosec
