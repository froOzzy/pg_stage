import datetime
import glob
import io
import os
import struct
import sys
import tempfile
import time
import zlib
from abc import ABCMeta, abstractmethod
from contextlib import suppress
from dataclasses import dataclass, field
from enum import Enum
from typing import BinaryIO, Iterator, Optional, Union

from pg_stage.obfuscators.plain import PlainObfuscator

Version = tuple[int, int, int]
DumpId = int
Offset = int


class PostgreSQLVersions:
    """Константы версий PostgreSQL для совместимости формата дампов."""

    V1_12 = (1, 12, 0)
    V1_13 = (1, 13, 0)
    V1_14 = (1, 14, 0)
    V1_15 = (1, 15, 0)
    V1_16 = (1, 16, 0)


class OffsetPosition:
    """Константы позиции смещения."""

    SET = 2
    NOT_SET = 1


class BlockType:
    """Идентификаторы типов блоков."""

    DATA = b'\x01'
    BLOBS = b'\x02'
    END = b'\x04'


class Constants:
    """Общие константы."""

    MAGIC_HEADER = b'PGDMP'
    CUSTOM_FORMAT = 1
    ZLIB_CHUNK_SIZE = 4096
    DEFAULT_BUFFER_SIZE = 1024 * 1024
    MAX_CHUNK_SIZE = 50 * 1024 * 1024
    PROCESSING_BUFFER_SIZE = 64 * 1024
    COMPRESSION_BUFFER_SIZE = 32 * 1024
    COMPRESSION_LEVEL = 6
    STREAM_WRITE_THRESHOLD = 10 * 1024 * 1024
    DEFAULT_TMP_DIR = os.getcwd()
    TMP_FILE_PREFIX = 'pg_dump_'


class PgDumpError(Exception):
    """Базовое исключение для ошибок обработки дампов PostgreSQL."""


class CompressionMethod(Enum):
    """Поддерживаемые методы сжатия."""

    NONE = 'none'
    GZIP = 'gzip'
    ZLIB = 'zlib'
    LZ4 = 'lz4'

    def __str__(self) -> str:
        return self.value


class SectionType(Enum):
    """Типы секций дампа."""

    PRE_DATA = 'SECTION_PRE_DATA'
    DATA = 'SECTION_DATA'
    POST_DATA = 'SECTION_POST_DATA'
    NONE = 'SECTION_NONE'


@dataclass(frozen=True)
class Header:
    """Информация заголовка файла дампа PostgreSQL."""

    magic: bytes
    version: Version
    database_name: str
    server_version: str
    pgdump_version: str
    compression_method: CompressionMethod
    create_date: datetime.datetime
    int_size: int = 4
    offset_size: int = 8


@dataclass(frozen=True)
class TocEntry:
    """Запись оглавления (Table of Contents)."""

    dump_id: DumpId
    section: SectionType
    had_dumper: bool
    tag: Optional[str] = None
    tablespace: Optional[str] = None
    namespace: Optional[str] = None
    tableam: Optional[str] = None
    owner: Optional[str] = None
    desc: Optional[str] = None
    defn: Optional[str] = None
    drop_stmt: Optional[str] = None
    copy_stmt: Optional[str] = None
    with_oids: Optional[str] = None
    oid: Optional[str] = None
    table_oid: Optional[str] = None
    data_state: int = 0
    offset: Offset = 0
    dependencies: list[DumpId] = field(default_factory=list)


@dataclass(frozen=True)
class Dump:
    """Полная структура файла дампа."""

    header: Header
    toc_entries: list[TocEntry]

    def get_table_data_entries(self) -> Iterator[TocEntry]:
        """
        Получить все записи данных таблиц.
        :return: итератор записей с данными таблиц
        """
        return (entry for entry in self.toc_entries if entry.desc == 'TABLE DATA')

    def get_comment_entries(self) -> Iterator[TocEntry]:
        """
        Получить все записи комментариев.
        :return: итератор записей комментариев
        """
        return (entry for entry in self.toc_entries if entry.desc == 'COMMENT')

    def get_entry_by_id(self, dump_id: DumpId) -> Optional[TocEntry]:
        """
        Найти запись TOC по ID дампа.
        :param dump_id: идентификатор записи в дампе
        :return: запись TOC или None
        """
        return next((entry for entry in self.toc_entries if entry.dump_id == dump_id), None)


class DataParser(metaclass=ABCMeta):
    """Протокол для реализации обработчиков данных."""

    @abstractmethod
    def parse(self, data: Union[str, bytes]) -> Union[str, bytes]:
        """
        Обработать данные и вернуть модифицированную версию.
        :param data: исходные данные (строка или байты)
        :return: обработанные данные
        """
        raise NotImplementedError()


class PgStageParser(DataParser):
    """Процессор обфускации из библиотеки pg_stage."""

    def __init__(self, parser, encoding: str = 'utf-8'):
        """
        Инициализация процессора обфускации.
        :param parser: функция парсинга из обфускатора
        :param encoding: кодировка для работы с текстом
        """
        self.encoding = encoding
        self.parser = parser

    def parse(self, data: Union[str, bytes]) -> Union[str, bytes]:
        """
        Применить замены текста к данным.
        :param data: исходные данные (строка или байты)
        :return: обработанные данные
        """
        if not data:
            return data

        if isinstance(data, str):
            return self.parser(line=data)

        try:
            lines = data.decode('utf-8').split('\n')
            processed_lines = []
            for line in lines:
                if line:
                    line = self.parser(line=line)

                if isinstance(line, str):
                    processed_lines.append(line)

            return '\n'.join(processed_lines).encode(self.encoding)
        except UnicodeDecodeError:
            return data


class StreamCombiner:
    """Объединяет несколько потоков в один последовательный поток."""

    def __init__(self, *streams: BinaryIO):
        """
        Инициализация с несколькими потоками.
        :param streams: потоки для объединения
        """
        self.streams = list(streams)
        self.current_index = 0

    def read(self, size: int = -1) -> bytes:
        """
        Чтение данных из потоков последовательно.
        :param size: количество байт для чтения
        :return: прочитанные данные
        """
        if self.current_index >= len(self.streams):
            return b''

        data = self.streams[self.current_index].read(size)

        if size != -1 and len(data) < size and data != b'':
            remaining = size - len(data)
            self.current_index += 1
            more_data = self.read(remaining)
            data += more_data
        elif not data:
            self.current_index += 1
            return self.read(size)

        return data


class DumpIO:
    """Утилиты бинарного I/O для формата дампов PostgreSQL."""

    def __init__(self, int_size: int = 4, offset_size: int = 8):
        """
        Инициализация с размерами типов данных.
        :param int_size: размер целого числа в байтах
        :param offset_size: размер смещения в байтах
        """
        self.int_size = int_size
        self.offset_size = offset_size

    def read_byte(self, stream: Union[BinaryIO, StreamCombiner]) -> int:
        """
        Чтение одного байта.
        :param stream: поток для чтения
        :return: значение байта
        """
        data = stream.read(1)
        if not data:
            message = 'Unexpected EOF while reading byte'
            raise PgDumpError(message)
        return struct.unpack('B', data)[0]

    def read_int(self, stream: Union[BinaryIO, StreamCombiner]) -> int:
        """
        Чтение знакового целого числа с переменным размером.
        :param stream: поток для чтения
        :return: значение целого числа
        """
        sign = self.read_byte(stream)
        value = 0

        for i in range(self.int_size):
            byte_value = self.read_byte(stream)
            if byte_value != 0:
                value += byte_value << (i * 8)

        return -value if sign else value

    def read_string(self, stream: Union[BinaryIO, StreamCombiner]) -> str:
        """
        Чтение строки UTF-8 с префиксом длины.
        :param stream: поток для чтения
        :return: строка
        """
        length = self.read_int(stream)
        if length <= 0:
            return ''

        data = stream.read(length)
        if len(data) != length:
            message = f'Expected {length} bytes, got {len(data)}'
            raise PgDumpError(message)

        try:
            return data.decode('utf-8')
        except UnicodeDecodeError as error:
            message = f'Invalid UTF-8 string: {error}'
            raise PgDumpError(message) from error

    def read_offset(self, stream: Union[BinaryIO, StreamCombiner]) -> Offset:
        """
        Чтение значения смещения.
        :param stream: поток для чтения
        :return: значение смещения
        """
        offset = 0
        for i in range(self.offset_size):
            byte_value = self.read_byte(stream)
            offset |= byte_value << (i * 8)
        return offset

    def write_int(self, value: int) -> bytes:
        """
        Запись знакового целого числа.
        :param value: значение для записи
        :return: байты для записи
        """
        is_negative = value < 0
        value = abs(value)

        result = bytearray()
        result.append(1 if is_negative else 0)

        for i in range(self.int_size):
            result.append((value >> (i * 8)) & 0xFF)

        return bytes(result)


class HeaderParser:
    """Парсер заголовков файлов дампов PostgreSQL."""

    def __init__(self, dio: DumpIO):
        """
        Инициализация парсера.
        :param dio: объект для работы с бинарным I/O
        """
        self.dio = dio

    def parse(self, stream: BinaryIO) -> Header:
        """
        Парсинг заголовка файла дампа.
        :param stream: поток для чтения
        :return: объект заголовка
        """
        magic = stream.read(5)
        if magic != Constants.MAGIC_HEADER:
            message = f'Invalid magic header: {magic!r}'
            raise PgDumpError(message)

        version = (self.dio.read_byte(stream), self.dio.read_byte(stream), self.dio.read_byte(stream))

        self._validate_version(version)

        int_size = self.dio.read_byte(stream)
        offset_size = self.dio.read_byte(stream)
        self.dio.int_size = int_size
        self.dio.offset_size = offset_size

        format_byte = self.dio.read_byte(stream)
        if format_byte != Constants.CUSTOM_FORMAT:
            message = f'Unsupported format: {format_byte}'
            raise PgDumpError(message)

        compression_method = self._parse_compression(stream, version)
        create_date = self._parse_date(stream)

        database_name = self.dio.read_string(stream)
        server_version = self.dio.read_string(stream)
        pgdump_version = self.dio.read_string(stream)

        return Header(
            magic=magic,
            version=version,
            database_name=database_name,
            server_version=server_version,
            pgdump_version=pgdump_version,
            compression_method=compression_method,
            create_date=create_date,
            int_size=int_size,
            offset_size=offset_size,
        )

    def _validate_version(self, version: Version) -> None:
        """
        Валидация версии формата дампа.
        :param version: версия для проверки
        """
        if version < PostgreSQLVersions.V1_12 or version > PostgreSQLVersions.V1_16:
            version_str = '.'.join(map(str, version))
            message = f'Unsupported version: {version_str}'
            raise PgDumpError(message)

    def _parse_compression(self, stream: BinaryIO, version: Version) -> CompressionMethod:
        """
        Парсинг метода сжатия в зависимости от версии.
        :param stream: поток для чтения
        :param version: версия формата
        :return: метод сжатия
        """
        if version >= PostgreSQLVersions.V1_15:
            compression_byte = self.dio.read_byte(stream)
            compression_map = {
                0: CompressionMethod.NONE,
                1: CompressionMethod.GZIP,
                2: CompressionMethod.LZ4,
                3: CompressionMethod.ZLIB,
            }
            compression_method = compression_map.get(compression_byte)
            if compression_method is None:
                message = f'Unknown compression method: {compression_byte}'
                raise PgDumpError(message)
        else:
            compression = self.dio.read_int(stream)
            if compression == -1:
                compression_method = CompressionMethod.ZLIB
            elif compression == 0:
                compression_method = CompressionMethod.NONE
            elif 1 <= compression <= 9:
                compression_method = CompressionMethod.GZIP
            else:
                message = f'Invalid compression level: {compression}'
                raise PgDumpError(message)

        return compression_method

    def _parse_date(self, stream: BinaryIO) -> datetime.datetime:
        """
        Парсинг даты создания из дампа.
        :param stream: поток для чтения
        :return: дата создания
        """
        sec = self.dio.read_int(stream)
        minute = self.dio.read_int(stream)
        hour = self.dio.read_int(stream)
        day = self.dio.read_int(stream)
        month = self.dio.read_int(stream)
        year = self.dio.read_int(stream)
        _isdst = self.dio.read_int(stream)

        try:
            return datetime.datetime(year=year + 1900, month=month + 1, day=day, hour=hour, minute=minute, second=sec)
        except ValueError as error:
            message = f'Invalid creation date: {error}'
            raise PgDumpError(message) from error


class TocParser:
    """Парсер записей оглавления (Table of Contents)."""

    def __init__(self, dio: DumpIO):
        """
        Инициализация парсера TOC.
        :param dio: объект для работы с бинарным I/O
        """
        self.dio = dio

    def parse(self, stream: BinaryIO, version: Version) -> list[TocEntry]:
        """
        Парсинг всех записей TOC.
        :param stream: поток для чтения
        :param version: версия формата дампа
        :return: список записей TOC
        """
        num_entries = self.dio.read_int(stream)
        return [self._parse_entry(stream, version) for _ in range(num_entries)]

    def _parse_entry(self, stream: BinaryIO, version: Version) -> TocEntry:
        """
        Парсинг одной записи TOC.
        :param stream: поток для чтения
        :param version: версия формата дампа
        :return: запись TOC
        """
        dump_id = self.dio.read_int(stream)
        had_dumper = bool(self.dio.read_int(stream))

        table_oid = self.dio.read_string(stream)
        oid = self.dio.read_string(stream)
        tag = self.dio.read_string(stream)
        desc = self.dio.read_string(stream)

        section_idx = self.dio.read_int(stream)
        section = self._parse_section(section_idx)

        defn = self.dio.read_string(stream)
        drop_stmt = self.dio.read_string(stream)
        copy_stmt = self.dio.read_string(stream)
        namespace = self.dio.read_string(stream)
        tablespace = self.dio.read_string(stream)

        tableam = None
        if version >= PostgreSQLVersions.V1_14:
            tableam = self.dio.read_string(stream)

        owner = self.dio.read_string(stream)
        with_oids = self.dio.read_string(stream)

        dependencies = self._parse_dependencies(stream)

        data_state = self.dio.read_byte(stream)
        offset = self.dio.read_offset(stream)

        return TocEntry(
            dump_id=dump_id,
            had_dumper=had_dumper,
            tag=tag or None,
            desc=desc or None,
            section=section,
            defn=defn or None,
            copy_stmt=copy_stmt or None,
            drop_stmt=drop_stmt or None,
            namespace=namespace or None,
            tablespace=tablespace or None,
            tableam=tableam,
            data_state=data_state,
            owner=owner or None,
            offset=offset,
            with_oids=with_oids or None,
            table_oid=table_oid or None,
            oid=oid or None,
            dependencies=dependencies,
        )

    def _parse_section(self, section_idx: int) -> SectionType:
        """
        Парсинг типа секции по индексу.
        :param section_idx: индекс секции
        :return: тип секции
        """
        section_map = {
            1: SectionType.PRE_DATA,
            2: SectionType.DATA,
            3: SectionType.POST_DATA,
            4: SectionType.NONE,
        }
        return section_map.get(section_idx, SectionType.NONE)

    def _parse_dependencies(self, stream: BinaryIO) -> list[DumpId]:
        """
        Парсинг списка зависимостей.
        :param stream: поток для чтения
        :return: список ID зависимостей
        """
        dependencies = []
        while True:
            dep_str = self.dio.read_string(stream)
            if not dep_str:
                break
            try:
                dependencies.append(int(dep_str))
            except ValueError:
                pass
        return dependencies


class StreamingLineBuffer:
    """Буфер для потоковой обработки строк с сохранением целостности."""

    def __init__(self):
        self._buffer = b''
        self._processed_size = 0

    def add_chunk(self, chunk: bytes) -> bytes:
        """
        Добавляет чанк данных и возвращает завершенные строки для обработки.
        :param chunk: новый чанк данных
        :return: завершенные строки для обработки
        """
        self._buffer += chunk

        last_newline = self._buffer.rfind(b'\n')
        if last_newline == -1:
            return b''

        complete_lines = self._buffer[: last_newline + 1]
        self._buffer = self._buffer[last_newline + 1 :]

        return complete_lines

    def get_remaining(self) -> bytes:
        """
        Возвращает оставшиеся данные в буфере.
        :return: незавершенные данные
        """
        return self._buffer

    def clear(self):
        """Очищает буфер."""
        self._buffer = b''


class DataBlockProcessor:
    """Обработчик блоков данных с поддержкой сжатия и потоковой обработки."""

    def __init__(self, dio: DumpIO, processor: DataParser):
        """
        Инициализация процессора блоков данных.
        :param dio: объект для работы с бинарным I/O
        :param processor: процессор данных
        """
        self.dio = dio
        self.processor = processor

    def process_block(
        self,
        input_stream: Union[BinaryIO, StreamCombiner],
        output_stream: BinaryIO,
        dump_id: DumpId,
        compression: CompressionMethod,
    ) -> None:
        """
        Обработка одного блока данных.
        :param input_stream: входной поток
        :param output_stream: выходной поток
        :param dump_id: ID записи дампа
        :param compression: метод сжатия
        """
        if compression == CompressionMethod.ZLIB:
            self._process_compressed_block(input_stream, output_stream, dump_id)
        else:
            self._process_uncompressed_block(input_stream, output_stream, dump_id)

    def _process_compressed_block(
        self,
        input_stream: Union[BinaryIO, StreamCombiner],
        output_stream: BinaryIO,
        dump_id: DumpId,
    ) -> None:
        """
        Потоковая обработка сжатого блока данных ZLIB без загрузки в память.
        :param input_stream: входной поток
        :param output_stream: выходной поток
        :param dump_id: ID записи дампа
        """
        decmop_prefix = f'{Constants.TMP_FILE_PREFIX}decomp_'
        proc_prefix = f'{Constants.TMP_FILE_PREFIX}proc_'
        decompressed_fd, decompressed_path = tempfile.mkstemp(prefix=decmop_prefix, dir=Constants.DEFAULT_TMP_DIR)
        processed_fd, processed_path = tempfile.mkstemp(prefix=proc_prefix, dir=Constants.DEFAULT_TMP_DIR)

        try:
            self._stream_decompress(input_stream, decompressed_fd)
            self._stream_process_lines(decompressed_path, processed_fd)
            self._stream_compress_and_write(processed_path, output_stream, dump_id)
        finally:
            for fd in [decompressed_fd, processed_fd]:
                if fd is not None:
                    with suppress(Exception):
                        os.close(fd)

            for path in [decompressed_path, processed_path]:
                if path and os.path.exists(path):
                    for _ in range(3):
                        try:
                            os.unlink(path)
                            break
                        except (OSError, PermissionError) as error:
                            time.sleep(0.1)

    def _stream_decompress(self, input_stream: Union[BinaryIO, StreamCombiner], output_fd: int) -> None:
        """
        Потоковая декомпрессия данных.
        :param input_stream: входной поток
        :param output_fd: файловый дескриптор для записи
        """
        decompressor = zlib.decompressobj()
        remaining_chunk = b''

        with os.fdopen(output_fd, 'wb') as output_file:
            while True:
                try:
                    chunk_size = self.dio.read_int(input_stream)
                except Exception as error:
                    message = f'Error reading chunk size: {error}'
                    raise PgDumpError(message) from error

                if chunk_size == 0:
                    break

                if chunk_size > Constants.MAX_CHUNK_SIZE:
                    message = f'Chunk size too large: {chunk_size}'
                    raise PgDumpError(message)

                chunk_data = input_stream.read(chunk_size)
                if len(chunk_data) != chunk_size:
                    message = f'Expected {chunk_size} bytes, got {len(chunk_data)}'
                    raise PgDumpError(message)

                remaining_chunk += chunk_data

                try:
                    decompressed_chunk = decompressor.decompress(remaining_chunk)
                    if decompressed_chunk:
                        output_file.write(decompressed_chunk)

                    remaining_chunk = decompressor.unconsumed_tail

                except zlib.error as error:
                    message = f'Decompression error: {error}'
                    raise PgDumpError(message) from error

                if chunk_size < Constants.ZLIB_CHUNK_SIZE:
                    break

            try:
                final_data = decompressor.flush()
                if final_data:
                    output_file.write(final_data)
            except zlib.error as error:
                message = f'Final decompression error: {error}'
                raise PgDumpError(message) from error

    def _stream_process_lines(self, input_path: str, output_fd: int) -> None:
        """
        Потоковая обработка данных с сохранением целостности строк.
        :param input_path: путь к файлу с данными для обработки
        :param output_fd: файловый дескриптор для записи результата
        """
        line_buffer = StreamingLineBuffer()

        with open(input_path, 'rb') as input_file:
            with os.fdopen(output_fd, 'wb') as output_file:
                while True:
                    chunk = input_file.read(Constants.PROCESSING_BUFFER_SIZE)
                    if not chunk:
                        remaining = line_buffer.get_remaining()
                        if remaining:
                            processed_data = self._process_data_chunk(remaining)
                            if processed_data:
                                output_file.write(processed_data)
                        break

                    complete_lines = line_buffer.add_chunk(chunk)
                    if complete_lines:
                        processed_data = self._process_data_chunk(complete_lines)
                        if processed_data:
                            output_file.write(processed_data)

    def _process_data_chunk(self, data: bytes) -> bytes:
        """
        Обрабатывает чанк данных через процессор.
        :param data: данные для обработки
        :return: обработанные данные
        """
        try:
            processed_data = self.processor.parse(data)
            if isinstance(processed_data, str):
                return processed_data.encode('utf-8')
            return processed_data
        except Exception as error:
            message = f'Processing error: {error}'
            raise PgDumpError(message) from error

    def _stream_compress_and_write(self, input_path: str, output_stream: BinaryIO, dump_id: DumpId) -> None:
        """
        Потоковая компрессия и запись результата.
        :param input_path: путь к файлу с обработанными данными
        :param output_stream: выходной поток
        :param dump_id: ID записи дампа
        """
        compressor = zlib.compressobj(level=Constants.COMPRESSION_LEVEL)

        output_stream.write(BlockType.DATA)
        output_stream.write(self.dio.write_int(dump_id))

        with open(input_path, 'rb') as input_file:
            while True:
                chunk = input_file.read(Constants.COMPRESSION_BUFFER_SIZE)
                if not chunk:
                    break

                compressed_chunk = compressor.compress(chunk)
                if compressed_chunk:
                    output_stream.write(self.dio.write_int(len(compressed_chunk)))
                    output_stream.write(compressed_chunk)

        final_compressed = compressor.flush()
        if final_compressed:
            output_stream.write(self.dio.write_int(len(final_compressed)))
            output_stream.write(final_compressed)

        output_stream.flush()

    def _process_uncompressed_block(
        self,
        input_stream: Union[BinaryIO, StreamCombiner],
        output_stream: BinaryIO,
        dump_id: DumpId,
    ) -> None:
        """
        Обработка несжатого блока данных с потоковой обработкой.
        :param input_stream: входной поток
        :param output_stream: выходной поток
        :param dump_id: ID записи дампа
        """
        size = self.dio.read_int(input_stream)

        if size > Constants.STREAM_WRITE_THRESHOLD:
            self._process_uncompressed_streaming(input_stream, output_stream, dump_id, size)
        else:
            data = input_stream.read(size)
            if len(data) != size:
                message = f'Expected {size} bytes, got {len(data)}'
                raise PgDumpError(message)

            processed_data = self.processor.parse(data)
            if isinstance(processed_data, str):
                processed_data = processed_data.encode('utf-8')

            self._write_data_block(output_stream, dump_id, processed_data)

    def _process_uncompressed_streaming(
        self,
        input_stream: Union[BinaryIO, StreamCombiner],
        output_stream: BinaryIO,
        dump_id: DumpId,
        total_size: int,
    ) -> None:
        """
        Потоковая обработка больших несжатых блоков.
        :param input_stream: входной поток
        :param output_stream: выходной поток
        :param dump_id: ID записи дампа
        :param total_size: общий размер блока
        """
        proc_uncomp_prefix = f'{Constants.TMP_FILE_PREFIX}uncompressed_'
        processed_fd, processed_path = tempfile.mkstemp(prefix=proc_uncomp_prefix, dir=Constants.DEFAULT_TMP_DIR)

        try:
            with os.fdopen(processed_fd, 'wb') as processed_file:
                line_buffer = StreamingLineBuffer()
                remaining_bytes = total_size

                while remaining_bytes > 0:
                    chunk_size = min(Constants.PROCESSING_BUFFER_SIZE, remaining_bytes)
                    chunk = input_stream.read(chunk_size)

                    if len(chunk) != chunk_size:
                        message = f'Expected {chunk_size} bytes, got {len(chunk)}'
                        raise PgDumpError(message)

                    remaining_bytes -= len(chunk)

                    complete_lines = line_buffer.add_chunk(chunk)
                    if complete_lines:
                        processed_data = self._process_data_chunk(complete_lines)
                        if processed_data:
                            processed_file.write(processed_data)

                remaining = line_buffer.get_remaining()
                if remaining:
                    processed_data = self._process_data_chunk(remaining)
                    if processed_data:
                        processed_file.write(processed_data)

                processed_file.flush()

            file_size = os.path.getsize(processed_path)
            output_stream.write(BlockType.DATA)
            output_stream.write(self.dio.write_int(dump_id))
            output_stream.write(self.dio.write_int(file_size))

            with open(processed_path, 'rb') as processed_file:
                while True:
                    chunk = processed_file.read(Constants.COMPRESSION_BUFFER_SIZE)
                    if not chunk:
                        break
                    output_stream.write(chunk)

            output_stream.flush()

        finally:
            for _ in range(3):
                try:
                    if processed_fd is not None:
                        os.close(processed_fd)

                    if processed_path and os.path.exists(processed_path):
                        os.unlink(processed_path)

                    break
                except (OSError, PermissionError) as error:
                    time.sleep(0.1)

    def _write_data_block(self, output_stream: BinaryIO, dump_id: DumpId, data: bytes) -> None:
        """
        Запись обработанного блока данных в выходной поток.
        :param output_stream: выходной поток
        :param dump_id: ID записи дампа
        :param data: данные для записи
        """
        output_stream.write(BlockType.DATA)
        output_stream.write(self.dio.write_int(dump_id))
        output_stream.write(self.dio.write_int(len(data)))
        output_stream.write(data)
        output_stream.flush()


class DumpProcessor:
    """Главный процессор дампов PostgreSQL с оптимизированной обработкой."""

    def __init__(self, data_parser: DataParser):
        """
        Инициализация процессора дампов.
        :param data_parser: обработчик данных
        """
        self.data_parser = data_parser
        self.dio = DumpIO()

    def process_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """
        Обработка дампа из входного потока в выходной поток.
        :param input_stream: входной поток
        :param output_stream: выходной поток
        """
        dump, combined_stream = self._parse_header_and_toc(input_stream, output_stream)
        self._process_data_blocks(combined_stream, output_stream, dump)

    def _parse_header_and_toc(self, input_stream: BinaryIO, output_stream: BinaryIO) -> tuple[Dump, StreamCombiner]:
        """
        Парсинг заголовка и TOC с записью в выходной поток.
        :param input_stream: входной поток
        :param output_stream: выходной поток
        :return: объект дампа и комбинированный поток
        """
        buffer = io.BytesIO()
        dump = None

        while dump is None:
            chunk = input_stream.read(Constants.DEFAULT_BUFFER_SIZE)
            if not chunk:
                message = 'Unexpected EOF while reading header/TOC'
                raise PgDumpError(message)

            buffer.write(chunk)
            buffer.seek(0)

            try:
                header_parser = HeaderParser(self.dio)
                header = header_parser.parse(buffer)

                toc_parser = TocParser(self.dio)
                toc_entries = toc_parser.parse(buffer, header.version)

                dump = Dump(header=header, toc_entries=toc_entries)

            except (PgDumpError, struct.error):
                buffer.seek(0, io.SEEK_END)
                continue

        toc_end_pos = buffer.tell()
        buffer.seek(0)

        header_toc_data = buffer.read(toc_end_pos)
        output_stream.write(header_toc_data)
        output_stream.flush()

        remaining_data = buffer.read()
        combined_stream = StreamCombiner(io.BytesIO(remaining_data), input_stream)

        return dump, combined_stream

    def _process_data_blocks(
        self,
        input_stream: Union[BinaryIO, StreamCombiner],
        output_stream: BinaryIO,
        dump: Dump,
    ) -> None:
        """
        Обработка блоков данных в дампе с прогресс-индикатором.
        :param input_stream: входной поток
        :param output_stream: выходной поток
        :param dump: объект дампа
        """
        dump_comments = {entry.defn for entry in dump.get_comment_entries() if entry.defn}
        for comment in dump_comments:
            with suppress(Exception):
                self.data_parser.parse(comment)

        table_data_entries = list(dump.get_table_data_entries())
        dump_copy_stmts = {entry.dump_id: entry.copy_stmt for entry in table_data_entries if entry.copy_stmt}
        dump_ids = {entry.dump_id for entry in table_data_entries}

        processor = DataBlockProcessor(self.dio, self.data_parser)

        while True:
            try:
                block_type = input_stream.read(1)
                if not block_type:
                    break

                if block_type == BlockType.DATA:
                    dump_id = self.dio.read_int(input_stream)

                    if dump_id in dump_ids:
                        copy_stmt = dump_copy_stmts.get(dump_id)
                        if copy_stmt:
                            with suppress(Exception):
                                self.data_parser.parse(copy_stmt)

                        try:
                            processor.process_block(
                                input_stream,
                                output_stream,
                                dump_id,
                                dump.header.compression_method,
                            )
                        except Exception as error:
                            message = f'Error processing data block {dump_id}: {error}'
                            raise PgDumpError(message) from error
                    else:
                        self._pass_through_block(input_stream, output_stream, block_type, dump_id)

                elif block_type == BlockType.END:
                    output_stream.write(block_type)
                    break
                else:
                    output_stream.write(block_type)

            except Exception as error:
                message = f'Error reading block: {error}'
                raise PgDumpError(message) from error

    def _pass_through_block(
        self,
        input_stream: Union[BinaryIO, StreamCombiner],
        output_stream: BinaryIO,
        block_type: bytes,
        dump_id: DumpId,
    ) -> None:
        """
        Передача блока без обработки с оптимизацией для больших блоков.
        :param input_stream: входной поток
        :param output_stream: выходной поток
        :param block_type: тип блока
        :param dump_id: ID записи дампа
        """
        output_stream.write(block_type)
        output_stream.write(self.dio.write_int(dump_id))

        size = self.dio.read_int(input_stream)
        output_stream.write(self.dio.write_int(size))

        remaining = size
        while remaining > 0:
            chunk_size = min(remaining, Constants.DEFAULT_BUFFER_SIZE)
            chunk = input_stream.read(chunk_size)
            if not chunk:
                message = f'Unexpected EOF while copying block data, {remaining} bytes remaining'
                raise PgDumpError(message)

            output_stream.write(chunk)
            remaining -= len(chunk)

        output_stream.flush()


class CustomObfuscator(PlainObfuscator):
    """Главный класс для работы с обфускатором."""

    @staticmethod
    def cleanup_tmp_files(*, prefix: str) -> None:
        """Удаляет файлы с указанным префиксом"""
        pattern = f'{prefix}*'
        files_to_delete = glob.glob(pattern)

        for file_name in files_to_delete:
            file_path = f'{Constants.DEFAULT_TMP_DIR}/{file_name}'
            try:
                if file_path and os.path.exists(file_path):
                    os.unlink(file_path)
            except OSError as e:
                message = f'Error cleaning up file {file_path}: {e}'
                raise PgDumpError(message) from e

    def run(self, *, stdin=None) -> None:
        """
        Метод для запуска обфускации.
        :param stdin: поток, с которого приходит информация в виде бинарных данных
        """
        if not stdin:
            stdin = sys.stdin

        if not isinstance(stdin, io.BufferedReader):
            stdin = stdin.buffer

        try:
            dump_processor = DumpProcessor(data_parser=PgStageParser(parser=self._parse_line))
            return dump_processor.process_stream(stdin, sys.stdout.buffer)
        finally:
            self.cleanup_tmp_files(prefix=Constants.TMP_FILE_PREFIX)
