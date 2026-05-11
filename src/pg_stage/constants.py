import os
from enum import Enum


class PostgreSQLVersions:
    """Константы версий PostgreSQL для совместимости формата дампов."""

    V1_12 = (1, 12, 0)
    V1_13 = (1, 13, 0)
    V1_14 = (1, 14, 0)
    V1_15 = (1, 15, 0)
    V1_16 = (1, 16, 0)


class BlockType:
    """Идентификаторы типов блоков."""

    DATA = b'\x01'
    BLOBS = b'\x02'
    END = b'\x04'


class Constants:
    """Общие константы."""

    MAGIC_HEADER = b'PGDMP'
    CUSTOM_FORMAT = 1
    ZLIB_CHUNK_SIZE = 1024 * 1024  # 1MB - увеличен для уменьшения системных вызовов
    DEFAULT_BUFFER_SIZE = 2 * 1024 * 1024  # 2MB для чтения блоков
    MAX_CHUNK_SIZE = 50 * 1024 * 1024
    PROCESSING_BUFFER_SIZE = 512 * 1024  # 512KB для обработки
    COMPRESSION_BUFFER_SIZE = 2 * 1024 * 1024  # 2MB для компрессии
    COMPRESSION_LEVEL = 6
    DEFAULT_TMP_DIR = os.getcwd()
    TMP_FILE_PREFIX = 'pg_dump_'
    LINE_BATCH_SIZE = 1000  # Количество строк для батчинга при записи


class CompressionMethod(Enum):
    """Поддерживаемые методы сжатия."""

    NONE = 'none'
    RAW = 'raw'
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
