import io
import json
import subprocess
from contextlib import redirect_stdout
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from pg_stage.constants import CompressionMethod, SectionType
from pg_stage.dataclasses import Dump, TocEntry
from pg_stage.exceptions import PgDumpError
from pg_stage.obfuscators.custom import CustomObfuscator, DumpIO, DumpProcessor, HeaderParser, PgStageParser, TocParser
from pg_stage.obfuscators.plain import PlainObfuscator
from tests.custom.helpers import pack_chunks, pack_int, read_block


@pytest.mark.parametrize('compression', [0, 6])
def test_real_archive_header(custom_fixtures: Path, compression: int) -> None:
    """
    Arrange: Настоящий custom-дамп PostgreSQL 17 без сжатия либо с gzip
    Act: Чтение заголовка через HeaderParser
    Assert: Версия формата, кодировка размеров и способ сжатия распознаны
    """
    with (custom_fixtures / f'postgres17-z{compression}.dump').open('rb') as stream:
        header = HeaderParser(DumpIO()).parse(stream)
    assert header.magic == b'PGDMP'
    assert header.version == (1, 16, 0)
    assert header.database_name == 'postgres'
    assert header.int_size == 4 and header.offset_size == 8
    assert header.compression_method == (CompressionMethod.NONE if compression == 0 else CompressionMethod.RAW)


@pytest.mark.parametrize('compression', [0, 6])
@pytest.mark.xfail(
    strict=True, raises=PgDumpError, reason='TocParser не учитывает дополнительные поля TABLE в формате 1.16'
)
def test_real_archive_toc(custom_fixtures: Path, compression: int) -> None:
    """
    Arrange: Настоящий custom-дамп с таблицами, комментариями и данными
    Act: Чтение заголовка и всего оглавления TOC
    Assert: Все пять таблиц данных и правила обфускации доступны в метаданных
    """
    with (custom_fixtures / f'postgres17-z{compression}.dump').open('rb') as stream:
        dio = DumpIO()
        header = HeaderParser(dio).parse(stream)
        entries = TocParser(dio).parse(stream, header.version)
    dump = Dump(header=header, toc_entries=entries)
    assert {entry.tag for entry in dump.get_table_data_entries()} == {
        'users',
        'deleted',
        'related_a',
        'related_b',
        'untouched',
    }
    assert any('anon:' in entry.defn for entry in dump.get_comment_entries() if entry.defn)


@pytest.mark.xfail(
    strict=True, raises=AssertionError, reason='DumpProcessor не сбрасывает состояние COPY между таблицами'
)
def test_archive_switches_table_context(custom_fixtures: Path) -> None:
    """
    Arrange: Два несжатых блока разных таблиц с собственными правилами обфускации
    Act: Последовательная обработка блоков через DumpProcessor без текстовых терминаторов COPY
    Assert: Каждый блок обработан по своим правилам и сохранил свой идентификатор
    """
    with (custom_fixtures / 'postgres17-z0.dump').open('rb') as stream:
        header = HeaderParser(DumpIO()).parse(stream)
    entries = []
    source = bytearray()
    for dump_id, table, column, value in [(1, 'users', 'name', 'first'), (2, 'peers', 'other_name', 'second')]:
        mutation = [{'mutation_name': 'random_choice', 'mutation_kwargs': {'choices': [value]}}]
        entries.append(
            TocEntry(
                dump_id=10 + dump_id,
                section=SectionType.NONE,
                had_dumper=False,
                desc='COMMENT',
                defn=f"COMMENT ON COLUMN public.{table}.{column} IS 'anon: {json.dumps(mutation)}';",
            )
        )
        entries.append(
            TocEntry(
                dump_id=dump_id,
                section=SectionType.DATA,
                had_dumper=True,
                desc='TABLE DATA',
                copy_stmt=f'COPY public.{table} (id, {column}) FROM stdin;',
            )
        )
        source.extend(b'\x01' + pack_int(dump_id) + pack_chunks(b'1\tprivate\n', compressed=False))
    dump = Dump(header=replace(header, compression_method=CompressionMethod.NONE), toc_entries=entries)
    output = io.BytesIO()
    DumpProcessor(PgStageParser(CustomObfuscator()._parse_line))._process_data_blocks(io.BytesIO(source), output, dump)
    output.seek(0)
    assert read_block(output, compressed=False) == (1, b'1\tfirst\n')
    assert read_block(output, compressed=False) == (2, b'1\tsecond\n')
    assert output.read() == b''


def table_rows(sql: str) -> dict[str, list[str]]:
    tables = {}
    current = None
    for line in sql.splitlines():
        if line.startswith('COPY '):
            current = line.split()[1]
            tables[current] = []
        elif line == '\\.':
            current = None
        elif current is not None:
            tables[current].append(line)
    return tables


@pytest.mark.parametrize('compression', [0, 6])
def test_real_fixture_is_readable(custom_fixtures: Path, pg_restore: str, compression: int) -> None:
    """
    Arrange: Тестовый архив, созданный штатным pg_dump PostgreSQL 17
    Act: Независимое преобразование архива в SQL через pg_restore
    Assert: Все таблицы и исходные строки доступны, архив не повреждён
    """
    sql = subprocess.check_output(
        [
            pg_restore,
            '--file=-',
            str(custom_fixtures / f'postgres17-z{compression}.dump'),
        ],
        text=True,
    )
    tables = table_rows(sql)
    assert len(tables) == 5
    assert tables['public.deleted'] == ['1\tprivate']
    assert len(tables['public.users']) == 2
    assert tables['public.untouched'] == ['1\tкириллица\\tтабуляция\\nстрока', '2\t\\N']


@pytest.mark.parametrize('compression', [0, 6])
@pytest.mark.xfail(strict=True, raises=PgDumpError, reason='Сквозной путь блокируется несовместимостью TOC 1.16')
def test_real_archive_matches_plain_restore(custom_fixtures: Path, pg_restore: str, compression: int) -> None:
    """
    Arrange: Реальный custom-дамп с мутациями, условиями, JSON, source_column, relations и удалением
    Act: Обфускация через публичный CustomObfuscator.run и декодирование результата штатным pg_restore
    Assert: Восстанавливаемые строки совпадают с результатом PlainObfuscator на том же дампе
    """
    original = (custom_fixtures / f'postgres17-z{compression}.dump').read_bytes()
    restored = subprocess.run([pg_restore, '--file=-'], input=original, capture_output=True, check=True).stdout.decode(
        'utf-8'
    )
    expected = io.StringIO()
    with redirect_stdout(expected):
        PlainObfuscator().run(stdin=io.StringIO(restored))
    output = io.BytesIO()
    with redirect_stdout(SimpleNamespace(buffer=output)):
        CustomObfuscator().run(stdin=io.BufferedReader(io.BytesIO(original)))
    result = subprocess.run(
        [pg_restore, '--file=-'],
        input=output.getvalue(),
        capture_output=True,
        check=True,
    ).stdout.decode('utf-8')
    assert table_rows(result) == table_rows(expected.getvalue())


def test_invalid_archive_header_raises() -> None:
    """
    Arrange: Входной поток без сигнатуры custom-архива PostgreSQL
    Act: Обработка через DumpProcessor
    Assert: Выбрасывается PgDumpError вместо выдачи повреждённого дампа
    """
    with pytest.raises(PgDumpError, match='Invalid magic header'):
        DumpProcessor(PgStageParser(CustomObfuscator()._parse_line)).process_stream(io.BytesIO(b'wrong'), io.BytesIO())
