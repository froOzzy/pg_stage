"""Временный PostgreSQL-кластер для генерации дампов и интеграционных тестов."""

import shlex
import shutil

# subprocess нужен для штатных PostgreSQL-утилит; оболочка не запускается.
import subprocess  # nosec B404
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

POSTGRES_TOOLS = frozenset({'initdb', 'pg_ctl', 'psql', 'createdb', 'pg_dump', 'pg_restore'})


def run_postgres(tool: str, *arguments: str, stdin_text: Optional[str] = None) -> subprocess.CompletedProcess[str]:
    """Запустить разрешённую PostgreSQL-утилиту по абсолютному пути без shell.

    PATH выбирает установленную разработчиком версию PostgreSQL; найденный путь
    разрешается до запуска. Имя утилиты проверяется по фиксированному списку,
    аргументы передаются отдельными элементами без интерпретации оболочкой.
    SQL для psql передаётся через stdin. Возвращает stdout/stderr как строки;
    отсутствие утилиты и ненулевой код возврата передаются вызывающему коду.
    """
    if tool not in POSTGRES_TOOLS:
        message = f'Unsupported PostgreSQL tool: {tool}'
        raise ValueError(message)
    executable = shutil.which(tool)
    if executable is None:
        message = f'PostgreSQL tool not found in PATH: {tool}'
        raise FileNotFoundError(message)
    command = [str(Path(executable).resolve(strict=True)), *arguments]
    # Фиксированный список утилит, абсолютный executable, аргументы без shell.
    return subprocess.run(  # nosec B603
        command,
        input=stdin_text,
        text=True,
        check=True,
        capture_output=True,
        shell=False,
    )


class Postgres:
    """Клиент временного кластера без TCP; все команды завершаются при SQL-ошибке.

    Кластер доступен только через Unix-сокет в приватном временном каталоге.
    Команды берутся из PATH; initdb, pg_ctl и клиент должны иметь одну версию.
    """

    def __init__(self, root: Path) -> None:
        self.root = root
        self.connection = ['-h', str(root), '-p', '55432', '-U', 'fixture']

    def create_database(self, name: str) -> None:
        """Создать пустую базу; передать ошибку createdb вызывающему коду."""
        run_postgres('createdb', *self.connection, name)

    def sql(self, database: str, sql: str) -> str:
        """Выполнить SQL или plain-дамп через psql; вернуть stdout без оформления."""
        return run_postgres(
            'psql',
            *self.connection,
            '-d',
            database,
            '-X',
            '-A',
            '-t',
            '-v',
            'ON_ERROR_STOP=1',
            stdin_text=sql,
        ).stdout

    def dump(self, database: str, destination: Path, *options: str) -> None:
        """Выгрузить базу штатным pg_dump с заданными форматом и сжатием."""
        run_postgres(
            'pg_dump',
            *self.connection,
            '-d',
            database,
            '--no-owner',
            '--no-privileges',
            *options,
            '-f',
            str(destination),
        )


@contextmanager
def postgres_cluster() -> Iterator[Postgres]:
    """Запустить изолированный кластер и остановить его даже при ошибке клиента.

    Требует PostgreSQL в PATH и непривилегированного пользователя. Каталог данных
    и сокет удаляются при выходе. Порт одинаков, но сокеты разных запусков изолированы.
    """
    with tempfile.TemporaryDirectory(prefix='pg-stage-') as directory:
        root = Path(directory)
        cluster = root / 'data'
        run_postgres(
            'initdb',
            '-D',
            str(cluster),
            '-U',
            'fixture',
            '--auth-local=trust',
            '--auth-host=reject',
            '--no-locale',
            '--encoding=UTF8',
        )
        try:
            run_postgres(
                'pg_ctl',
                '-D',
                str(cluster),
                '-l',
                str(root / 'postgres.log'),
                '-o',
                f"-F -h '' -k {shlex.quote(str(root))} -p 55432",
                '-w',
                'start',
            )
            yield Postgres(root)
        finally:
            # При неудачном старте сервер мог успеть создать postmaster.pid.
            if (cluster / 'postmaster.pid').exists():
                run_postgres('pg_ctl', '-D', str(cluster), '-m', 'immediate', '-w', 'stop')
