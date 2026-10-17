import io
import json
import os
from contextlib import redirect_stdout

import pytest

from pg_stage.constants import CompressionMethod
from pg_stage.obfuscators.custom import CustomObfuscator, DataBlockProcessor, DumpIO, PgStageParser
from pg_stage.obfuscators.plain import PlainObfuscator
from tests.custom.helpers import pack_chunks, unpack_block


def scenario(name):
    mutation = {'mutation_name': 'random_choice', 'mutation_kwargs': {'choices': ['hidden']}}
    column = 'name'
    columns = 'token, id, name, status, details'
    rows = 'old-1\t1\tАлиса\tactive\t{"secret":"private","keep":42}\nold-2\t2\tБорис\tinactive\t\\N\n'
    mutations = [mutation]
    if name in ('equal', 'not_equal', 'by_pattern'):
        mutation['conditions'] = [
            {'column_name': 'status', 'operation': name, 'value': '^active$' if name == 'by_pattern' else 'active'}
        ]
    elif name == 'two_mutations':
        mutation['conditions'] = [{'column_name': 'status', 'operation': 'equal', 'value': 'active'}]
        mutations.append({'mutation_name': 'random_choice', 'mutation_kwargs': {'choices': ['fallback']}})
    elif name == 'source_column':
        column = 'token'
        mutations = [
            {
                'mutation_name': 'uuid5_by_source_value',
                'mutation_kwargs': {'source_column': 'name', 'namespace': '6ba7b810-9dad-11d1-80b4-00c04fd430c8'},
            }
        ]
    elif name == 'json':
        column = 'details'
        mutations = [{'mutation_name': 'json_update', 'mutation_kwargs': {'mutations_by_key': {'secret': [mutation]}}}]
    comments = [f"COMMENT ON COLUMN public.users.{column} IS 'anon: {json.dumps(mutations)}';"]
    if name == 'passthrough':
        comments = []
    elif name == 'delete':
        comments = ['COMMENT ON TABLE public.users IS \'anon: {"mutation_name":"delete"}\';']
    options = {'delete_tables_by_pattern': [r'^public\.users$']} if name == 'delete_pattern' else {}
    return comments, f'COPY public.users ({columns}) FROM stdin;', rows, options


@pytest.mark.parametrize(
    'case',
    [
        'passthrough',
        'mutation',
        'equal',
        'not_equal',
        'by_pattern',
        'two_mutations',
        'source_column',
        'json',
        pytest.param(
            'delete',
            marks=pytest.mark.xfail(
                strict=True, raises=AssertionError, reason='None не удаляет строку в PgStageParser'
            ),
        ),
        pytest.param(
            'delete_pattern',
            marks=pytest.mark.xfail(
                strict=True, raises=AssertionError, reason='None не удаляет строку в PgStageParser'
            ),
        ),
    ],
)
@pytest.mark.parametrize('chunk_size', [1, 7, 4096])
def test_uncompressed_block_matches_plain(case: str, chunk_size: int) -> None:
    """
    Arrange: Правила и строки из сценариев plain-обфускатора, упакованные в бинарные чанки
    Act: Обработка несжатого блока и тех же строк текстовым обфускатором
    Assert: Байтовый результат совпадает с plain, сохранены ID блока и нулевой терминатор
    """
    check_block_matches_plain(case, chunk_size, CompressionMethod.NONE)


@pytest.mark.parametrize(
    'case',
    [
        'passthrough',
        'mutation',
        'equal',
        'not_equal',
        'by_pattern',
        'two_mutations',
        'source_column',
        'delete',
        'delete_pattern',
    ],
)
@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason='Сжатый путь теряет границы строк и не записывает нулевой терминатор блока',
)
def test_compressed_block_matches_plain(case: str) -> None:
    """
    Arrange: Сценарий plain-обфускатора в сжатом бинарном блоке
    Act: Обработка сжатого блока и независимое чтение результата
    Assert: Архивный блок корректно завершён, строки совпадают с plain-результатом
    """
    check_block_matches_plain(case, 1024 * 1024, CompressionMethod.ZLIB)


@pytest.mark.xfail(
    strict=True, raises=ValueError, reason='Сжатый путь склеивает строки и передаёт невалидный JSON в мутацию'
)
def test_compressed_json_matches_plain() -> None:
    """
    Arrange: Сжатый блок с JSON-полем в нескольких строках
    Act: Обработка блока через штатный потоковый парсер
    Assert: JSON каждой строки обрабатывается независимо, результат совпадает с plain
    """
    check_block_matches_plain('json', 1024 * 1024, CompressionMethod.ZLIB)


def check_block_matches_plain(case: str, chunk_size: int, compression: CompressionMethod) -> None:
    comments, copy, rows, options = scenario(case)
    plain = PlainObfuscator(**options)
    expected = io.StringIO()
    with redirect_stdout(expected):
        plain.run(stdin=io.StringIO('\n'.join([*comments, copy]) + '\n' + rows + '\\.\n'))
    expected_rows = expected.getvalue().split(copy + '\n', 1)[1].removesuffix('\\.\n').encode('utf-8')
    custom = CustomObfuscator(**options)
    for comment in comments:
        custom._parse_line(line=comment)
    custom._parse_copy_values(line=copy)
    compressed = compression != CompressionMethod.NONE
    source = io.BytesIO(pack_chunks(rows.encode('utf-8'), compressed=compressed, chunk_size=chunk_size))
    output = io.BytesIO()
    DataBlockProcessor(DumpIO(), PgStageParser(custom._parse_line)).process_block(
        source,
        output,
        42,
        compression,
    )
    assert unpack_block(output.getvalue(), compressed=compressed) == (42, expected_rows)
    assert source.read() == b''


@pytest.mark.parametrize('self_relation', [False, True])
def test_uncompressed_related_columns(*, self_relation: bool) -> None:
    """
    Arrange: Две связанные колонки одной таблицы либо двух таблиц с разным порядком полей
    Act: Обработка бинарных блоков с генерацией и повторным использованием соответствий
    Assert: Обе колонки содержат одно обфусцированное значение для каждого ключа
    """
    custom = CustomObfuscator()
    other = 'public.users' if self_relation else 'public.peers'
    for table, column, target_table, target_column, choice in [
        ('public.users', 'name', other, 'other_name', 'shared'),
        (other, 'other_name', 'public.users', 'name', 'different'),
    ]:
        mutation = [
            {
                'mutation_name': 'random_choice',
                'mutation_kwargs': {'choices': [choice]},
                'relations': [
                    {
                        'table_name': target_table,
                        'column_name': target_column,
                        'from_column_name': 'id',
                        'to_column_name': 'id',
                    }
                ],
            }
        ]
        custom._parse_line(line=f"COMMENT ON COLUMN {table}.{column} IS 'anon: {json.dumps(mutation)}';")
    parser = PgStageParser(custom._parse_line)

    def process(copy, rows):
        # Проверка DataBlockProcessor: метаданные блока устанавливаются отдельно от DumpProcessor.
        custom._parse_copy_values(line=copy)
        output = io.BytesIO()
        DataBlockProcessor(DumpIO(), parser).process_block(
            io.BytesIO(pack_chunks(rows, compressed=False, chunk_size=3)),
            output,
            7,
            CompressionMethod.NONE,
        )
        return unpack_block(output.getvalue(), compressed=False)[1]

    if self_relation:
        assert (
            process(
                'COPY public.users (id, name, other_name) FROM stdin;', b'1\tprivate\tprivate\n2\tprivate\tprivate\n'
            )
            == b'1\tshared\tshared\n2\tshared\tshared\n'
        )
    else:
        assert (
            process('COPY public.users (id, name) FROM stdin;', b'1\tprivate\n2\tprivate\n')
            == b'1\tshared\n2\tshared\n'
        )
        assert (
            process('COPY public.peers (other_name, id) FROM stdin;', b'private\t1\nprivate\t2\n')
            == b'shared\t1\nshared\t2\n'
        )


@pytest.mark.xfail(
    strict=True, raises=AssertionError, reason='_process_single_line убирает перевод строки перед потоковым парсером'
)
def test_compressed_line_processing_preserves_rows(tmp_path) -> None:
    """
    Arrange: Файл с распакованными строками и парсер, ожидающий границы строк
    Act: Построчная обработка файла как в сжатой ветке
    Assert: Строки не склеены, обработаны независимо и выданы с исходными границами
    """
    path = tmp_path / 'input'
    path.write_bytes(b'one\ntwo\n')
    fd = os.open(tmp_path / 'output', os.O_WRONLY | os.O_CREAT, 0o600)
    processor = DataBlockProcessor(DumpIO(), PgStageParser(lambda *, line: line.upper()))
    processor._stream_process_lines(str(path), fd)
    assert (tmp_path / 'output').read_bytes() == b'ONE\nTWO\n'


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason='Сжатый блок не получает нулевой терминатор',
)
def test_compressed_block_is_complete() -> None:
    """
    Arrange: Сжатый блок с одним чанком и обработчиком без изменений данных
    Act: Обработка сжатого блока и независимая распаковка результата
    Assert: Блок содержит все строки и завершается нулевой длиной чанка
    """

    class IdentityParser:
        def parse(self, data):
            return data

    payload = b'one\ntwo\nthree\n'
    output = io.BytesIO()
    source = io.BytesIO(pack_chunks(payload, compressed=True, chunk_size=1024))
    DataBlockProcessor(DumpIO(), IdentityParser()).process_block(source, output, 8, CompressionMethod.ZLIB)
    assert unpack_block(output.getvalue(), compressed=True) == (8, payload)
    assert source.read() == b''


@pytest.mark.xfail(
    strict=True, raises=AssertionError, reason='Декомпрессия прекращается при чанке меньше 1 МиБ, не дожидаясь нуля'
)
def test_decompression_reads_all_chunks(tmp_path) -> None:
    """
    Arrange: Сжатый поток разбит на несколько чанков меньше размера внутреннего буфера
    Act: Декомпрессия в файл до нулевого терминатора
    Assert: Все данные распакованы, входной поток полностью прочитан
    """
    payload = b'one\ntwo\nthree\n'
    source = io.BytesIO(pack_chunks(payload, compressed=True, chunk_size=7))
    path = tmp_path / 'decompressed'
    fd = os.open(path, os.O_WRONLY | os.O_CREAT, 0o600)
    DataBlockProcessor(DumpIO(), PgStageParser(lambda *, line: line))._stream_decompress(source, fd)
    assert path.read_bytes() == payload
    assert source.read() == b''
