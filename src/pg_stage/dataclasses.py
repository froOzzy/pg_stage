import datetime
from dataclasses import dataclass, field
from typing import Iterator, Optional

from pg_stage.contstants import CompressionMethod, SectionType
from pg_stage.types import DumpId, Offset, Version


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
