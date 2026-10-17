import json
import uuid
from datetime import date

import pytest

from src.pg_stage.obfuscators.plain import PlainObfuscator


@pytest.mark.parametrize('configured_context', [False, True])
@pytest.mark.parametrize('with_relations', [False, True])
def test_mutation_context_is_fresh_for_each_row(
    obfuscator_object: PlainObfuscator,
    monkeypatch: pytest.MonkeyPatch,
    *,
    configured_context: bool,
    with_relations: bool,
) -> None:
    """
    Arrange: Мутация с source_column, опциональными relations и явно заданным контекстом
    Act: Обработка двух строк с разными значениями и ключами связи
    Assert: Каждая строка получает свой контекст, явные параметры сохранены, конфигурация не изменена
    """
    received = []

    def mutate(**kwargs) -> str:
        received.append((kwargs['current_value'], dict(kwargs['obfuscated_values'])))
        return f'{kwargs["current_value"]}:{kwargs["obfuscated_values"]["name"]}'

    monkeypatch.setattr(obfuscator_object._mutator, 'mutation_echo', mutate, raising=False)
    mutation_kwargs = {'source_column': 'name'}
    if configured_context:
        mutation_kwargs.update(current_value='fixed', obfuscated_values={'name': 'configured'})
    mutation = {'mutation_name': 'echo', 'mutation_kwargs': mutation_kwargs}
    if with_relations:
        mutation['relations'] = [
            {
                'table_name': 'peers',
                'column_name': 'value',
                'from_column_name': 'id',
                'to_column_name': 'id',
            }
        ]
    obfuscator_object._parse_line(
        line=f"COMMENT ON COLUMN users.value IS 'anon: {json.dumps([mutation])}';",
    )
    obfuscator_object._parse_line(line='COPY users (value, id, name) FROM stdin;')

    results = [
        obfuscator_object._parse_line(line='first\t1\tAlice'),
        obfuscator_object._parse_line(line='second\t2\tBob'),
    ]

    if configured_context:
        assert results == ['fixed:configured\t1\tAlice', 'fixed:configured\t2\tBob']
        assert received == [('fixed', {'name': 'configured'}), ('fixed', {'name': 'configured'})]
    else:
        assert results == ['first:Alice\t1\tAlice', 'second:Bob\t2\tBob']
        assert received == [('first', {'id': '1', 'name': 'Alice'}), ('second', {'id': '2', 'name': 'Bob'})]
    assert obfuscator_object._map_tables['users']['value'][0]['mutation_kwargs'] == mutation_kwargs


def test_conditions_use_original_values(obfuscator_object: PlainObfuscator) -> None:
    """
    Arrange: Дамп с мутацией статуса и условной мутацией email на основе исходного статуса
    Act: Вызов функции `_parse_line` для строк данных и перехода к таблице без мутаций
    Assert: Условия используют исходный статус, остальные поля и данные следующей таблицы сохранены
    """
    rules = {
        'status': [{'mutation_name': 'random_choice', 'mutation_kwargs': {'choices': ['changed']}}],
        'email': [
            {
                'mutation_name': 'random_choice',
                'mutation_kwargs': {'choices': ['hidden']},
                'conditions': [{'column_name': 'status', 'operation': 'equal', 'value': 'original'}],
            }
        ],
    }
    for column, mutations in rules.items():
        obfuscator_object._parse_line(
            line=f"COMMENT ON COLUMN users.{column} IS 'anon: {json.dumps(mutations)}';",
        )
    obfuscator_object._parse_line(line='COPY users (id, status, email, notes, empty) FROM stdin;')

    assert obfuscator_object._parse_line(line='1\toriginal\tprivate\t\\N\t') == '1\tchanged\thidden\t\\N\t'
    assert obfuscator_object._parse_line(line='2\tother\tprivate\tliteral\\ttext\t') == (
        '2\tchanged\tprivate\tliteral\\ttext\t'
    )
    obfuscator_object._parse_line(line='\\.')
    obfuscator_object._parse_line(line='COPY untouched (id, name) FROM stdin;')
    assert obfuscator_object._parse_line(line='3\toriginal') == '3\toriginal'


@pytest.mark.parametrize('mutate_source', [False, True])
def test_source_column_context_preserves_column_order(
    obfuscator_object: PlainObfuscator,
    *,
    mutate_source: bool,
) -> None:
    """
    Arrange: Дамп с UUID на основе колонки, расположенной после него, с мутацией источника или без неё
    Act: Вызов функции `_parse_line` для строки данных
    Assert: UUID вычислен по итоговому значению источника, порядок колонок и остальные поля сохранены
    """
    namespace = uuid.NAMESPACE_DNS
    mutation = [
        {
            'mutation_name': 'uuid5_by_source_value',
            'mutation_kwargs': {'source_column': 'name', 'namespace': str(namespace)},
        }
    ]
    obfuscator_object._parse_line(
        line=f"COMMENT ON COLUMN users.token IS 'anon: {json.dumps(mutation)}';",
    )
    if mutate_source:
        mutation = [{'mutation_name': 'random_choice', 'mutation_kwargs': {'choices': ['hidden']}}]
        obfuscator_object._parse_line(
            line=f"COMMENT ON COLUMN users.name IS 'anon: {json.dumps(mutation)}';",
        )
    obfuscator_object._parse_line(line='COPY users (token, id, name, notes) FROM stdin;')

    name = 'hidden' if mutate_source else 'original'
    token = uuid.uuid5(namespace, f'{name}-{date.today()}')
    assert obfuscator_object._parse_line(line='old-token\t1\toriginal\t\\N') == f'{token}\t1\t{name}\t\\N'


def test_parse_copy_values_with_delete_table(obfuscator_object: PlainObfuscator) -> None:
    """
    Arrange: Дамп таблиц, данные которых необходимо удалить
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout нет данных из таблицы
    """
    with open('tests/sql/test_parse_copy_values_with_delete_tables.sql') as file:
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
    assert assert_result == result  # nosec


def test_parse_copy_values_with_mutation(obfuscator_object: PlainObfuscator) -> None:
    """
    Arrange: Дамп таблиц, в которых необходимо мутировать одно или несколько полей
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout данные полей мутированы
    """
    with open('tests/sql/test_parse_copy_values_with_mutation.sql') as file:
        dump_sql = file.read()

    emails = {
        'cj@example.com',
        'leo@example.com',
        'donna@example.com',
        'charlie@example.com',
        'fun@example.com',
    }
    birthdays = {'1996-10-02', '1996-10-03', '2005-01-02', '2005-10-02', '2022-12-31'}
    tokens = {
        '86a97ff982e87ed5af7d90ab2ce31d4e89a3af3e6a0490b067bb8213aea7a4ee0eeafae1d8fe3c6f990aead095092fcf852004b18'
        'e484ef22569aebf64c3747f',
        '630aaf10f3edcb396181535476bccfd369e1ee9281cbc218d0861e6117b9839219cb403abed3b59468b2564c229d78b0cb610d0e1'
        '6fa4a03dc4d93ed3d55deb3',
        '06fa5d0f3a4d62ff60717ff3315301129a5bcd152f63f073b67d2e6a835b098524b1d097367283c97ca75db9154cf61d6a918248e'
        'b68eaf8cd83d1a87cdd92dc',
        '02cbd8d1e9690c7786375f9f6ec4da6fa3c2ead70d41a7aa1d7fe631477b42635210f0e8fa7579f6f4b5afdb364d9465623a2861e'
        'cff75fa3a052c9b2a9fc2dd',
        'b09909b6e83938dd41ffb5e931eeb3d646b1856dfb74a81acb1697b6d8466468047fe92286e011a4634c71b8d8775c7d5a31e19ce'
        '111bd31d0a61a4faf93d6af',
    }
    crypted_password = (  # nosec
        '400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3125d3bd1ett18ffc4a8092e2616b9e5ca7954b2c52504'
    )
    password_salts = {
        'v8BMktHnOeokEBTy6As',
        'c5d6v3NS97D3wYkUltFQ',
        '2IcBeSh6IVVCJyZpqBt',
        'QOqWQ24CMiRNuPUz8f5',
        'uMYA6c3A7uGoI0aEbJ8R',
    }

    for line in dump_sql.splitlines():
        new_line = obfuscator_object._parse_line(line=line)
        if new_line and 'COPY' not in new_line and 'COMMENT' not in new_line and '\\.' not in line:
            assert not any(email in new_line for email in emails)  # nosec
            assert not any(birthday in new_line for birthday in birthdays)  # nosec
            assert not any(token in new_line for token in tokens)  # nosec
            assert not any(password_salt in new_line for password_salt in password_salts)  # nosec
            assert crypted_password in new_line  # nosec


def test_parse_copy_values_with_relations(obfuscator_object: PlainObfuscator) -> None:
    """
    Arrange: Дамп таблиц, в которых необходимо мутировать одно связанное поле
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout данные поле мутировано во всех таблицах одинаково и не задета таблица с похожими данными
    """
    with open('tests/sql/test_parse_copy_values_with_relations.sql') as file:
        dump_sql = file.read()

    result = []
    for line in dump_sql.splitlines():
        new_line = obfuscator_object._parse_line(line=line)
        if new_line is not None:
            result.append(new_line)

    index_copy_table4 = result.index('20f654fe-b27d-4051-9fd4-000000000001\t111n\tLourense') - 1
    assert 'table_4' in result[index_copy_table4]  # nosec
    assert (  # nosec
        len(
            [line for line in result if line == '20f654fe-b27d-4051-9fd4-000000000001\t111n\tLourense'],
        )
        == 1
    )
    assert (
        len(
            [line for line in result if line == '20f654fe-b27d-4051-9fd4-000000000002\t222n\tKent'],
        )
        == 1
    )  # nosec
    assert (  # nosec
        len(
            {line for line in result if '20f654fe-b27d-4051-9fd4-000000000001' in line and '111n' not in line},
        )
        == 1
    )
    assert (  # nosec
        len(
            {line for line in result if '20f654fe-b27d-4051-9fd4-000000000002' in line and '222n' not in line},
        )
        == 1
    )


def test_parse_copy_values_with_self_relation(obfuscator_object: PlainObfuscator) -> None:
    """
    Arrange: Дамп таблицы, в которой необходимо мутировать данные с связанным полем внутри таблицы
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout данные поле мутировано в двух столбцах одинаково
    """
    with open('tests/sql/test_parse_copy_values_with_self_relation.sql') as file:
        dump_sql = file.read()

    result = []
    for line in dump_sql.splitlines():
        new_line = obfuscator_object._parse_line(line=line)
        if new_line is not None:
            result.append(new_line)

    prepared_result = [
        line.split('\t')[1:]
        for line in result
        if '20f654fe-b27d-4051-9fd4-000000000001' in line or '20f654fe-b27d-4051-9fd4-000000000002' in line
    ]
    assert prepared_result[0][0] == prepared_result[0][1]  # nosec
    assert prepared_result[1][0] == prepared_result[1][1]  # nosec


@pytest.mark.parametrize('table_order', [('source', 'target'), ('target', 'source')])
def test_relations_with_multiple_keys_and_different_column_order(
    obfuscator_object: PlainObfuscator,
    monkeypatch: pytest.MonkeyPatch,
    table_order: tuple[str, str],
) -> None:
    """
    Arrange: Две связанные таблицы с разным порядком колонок и двумя ключами связи
    Act: Обработка таблиц в разном порядке с совпадением только по второму ключу
    Assert: Значения согласованы по каждой связи, мутация вызывается только для первой таблицы
    """
    generated = []

    def mutate(**kwargs: str) -> str:
        value = f'hidden-{kwargs["current_value"]}'
        generated.append(value)
        return value

    monkeypatch.setattr(obfuscator_object._mutator, 'mutation_first_name', mutate)
    for table, other, from_columns, to_columns in [
        ('source', 'target', ['id', 'alternate_id'], ['ref', 'alternate_ref']),
        ('target', 'source', ['ref', 'alternate_ref'], ['id', 'alternate_id']),
    ]:
        mutation = [
            {
                'mutation_name': 'first_name',
                'relations': [
                    {
                        'table_name': other,
                        'column_name': 'name',
                        'from_column_name': from_column,
                        'to_column_name': to_column,
                    }
                    for from_column, to_column in zip(from_columns, to_columns)
                ],
            }
        ]
        obfuscator_object._parse_line(
            line=f"COMMENT ON COLUMN {table}.name IS 'anon: {json.dumps(mutation)}';",
        )

    copy_statements = {
        'source': 'COPY source (name, id, alternate_id) FROM stdin;',
        'target': 'COPY target (alternate_ref, name, ref) FROM stdin;',
    }
    rows = {
        'source': ['Alice\t1\ta', 'Bob\t2\tb'],
        'target': ['a\tCarol\tmissing-1', 'b\tDave\tmissing-2'],
    }
    results = {}
    for table in table_order:
        obfuscator_object._parse_line(line=copy_statements[table])
        results[table] = [obfuscator_object._parse_line(line=row) for row in rows[table]]
        obfuscator_object._parse_line(line='\\.')

    names = ['hidden-Alice', 'hidden-Bob'] if table_order[0] == 'source' else ['hidden-Carol', 'hidden-Dave']
    assert results['source'] == [f'{names[0]}\t1\ta', f'{names[1]}\t2\tb']
    assert results['target'] == [f'a\t{names[0]}\tmissing-1', f'b\t{names[1]}\tmissing-2']
    assert generated == names


def test_two_mutation_for_one_column(obfuscator_object: PlainObfuscator) -> None:
    """
    Arrange: Дамп таблицы, в которой необходимо мутировать данные с двумя видами мутации
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout данные поля мутированы
    """
    with open('tests/sql/test_two_mutation_for_one_column.sql') as file:
        dump_sql = file.read()

    result = []
    for line in dump_sql.splitlines():
        new_line = obfuscator_object._parse_line(line=line)
        if new_line is not None:
            result.append(new_line)

    prepared_result = [
        line.split('\t')[1:]
        for line in result
        if '20f654fe-b27d-4051-9fd4-000000000001' in line
        or '20f654fe-b27d-4051-9fd4-000000000002' in line
        or '20f654fe-b27d-4051-9fd4-000000000003' in line
    ]

    assert prepared_result[0][0] != '79999999999'  # nosec
    assert prepared_result[1][0] != 'test@mail.ru'  # nosec
    assert prepared_result[2][0] != '89999999999'  # nosec


def test_obfuscate_uuid_by_source_column(obfuscator_object: PlainObfuscator) -> None:
    """
    Arrange: Дамп таблицы, в которой определены мутации uuid на основе мутации другой колонки
    Act: Вызов функции `_parse_line` класса Obfuscator
    Assert: В stdout данные поля мутированы на основе мутированного значения другой колонки
    """
    with open('tests/sql/test_obfuscate_uuid_by_source_value.sql') as file:
        dump_sql = file.read()

    result = []
    for line in dump_sql.splitlines():
        new_line = obfuscator_object._parse_line(line=line)
        if new_line is not None:
            result.append(new_line)

    prepared_result = [line.split('\t') for line in result if '111n' in line or '222n' in line or '333n' in line]

    date_today = date.today()
    uuid_namespace = uuid.UUID(str('6ba7b810-9dad-11d1-80b4-00c04fd430c8'))
    for column_uuid, phone, _ in prepared_result:
        assert column_uuid == str(uuid.uuid5(uuid_namespace, f'{phone}-{date_today}'))  # nosec
