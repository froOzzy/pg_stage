from src.pg_stage.obfuscator import Obfuscator


def test_equal_condition(obfuscator_object: Obfuscator):
    """
    Arrange: Дамп таблиц, данные в которой необходимо обфусцировать
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout обфусцированы только те данные, условия которых выполняются
    """
    with open('tests/sql/test_equal_condition.sql') as file:
        dump_sql = file.read()

    for line in dump_sql.splitlines():
        new_line = obfuscator_object._parse_line(line=line)
        if new_line is not None:
            if new_line.startswith('1'):
                assert 'test@mail.ru' not in new_line  # nosec

            if new_line.startswith('2'):
                assert 'test@mail.ru' in new_line  # nosec


def test_not_equal_condition(obfuscator_object: Obfuscator):
    """
    Arrange: Дамп таблиц, данные в которой необходимо обфусцировать
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout обфусцированы только те данные, условия которых выполняются
    """
    with open('tests/sql/test_not_equal_condition.sql') as file:
        dump_sql = file.read()

    for line in dump_sql.splitlines():
        new_line = obfuscator_object._parse_line(line=line)
        if new_line is not None:
            if new_line.startswith('1'):
                assert 'test@mail.ru' in new_line  # nosec

            if new_line.startswith('2'):
                assert 'test@mail.ru' not in new_line  # nosec


def test_by_pattern_condition(obfuscator_object: Obfuscator):
    """
    Arrange: Дамп таблиц, данные в которой необходимо обфусцировать
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout обфусцированы только те данные, условия которых выполняются
    """
    with open('tests/sql/test_by_pattern_condition.sql') as file:
        dump_sql = file.read()

    for line in dump_sql.splitlines():
        new_line = obfuscator_object._parse_line(line=line)
        if new_line is not None:
            if new_line.startswith('1'):
                assert 'test@mail.ru' not in new_line  # nosec

            if new_line.startswith('2'):
                assert 'test@mail.ru' not in new_line  # nosec
