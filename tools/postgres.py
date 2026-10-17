"""Временный PostgreSQL-кластер для генерации дампов и интеграционных тестов."""

import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


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
        subprocess.run(['createdb', *self.connection, name], check=True, capture_output=True)

    def sql(self, database: str, sql: str) -> str:
        """Выполнить SQL или plain-дамп через psql; вернуть stdout без оформления."""
        return subprocess.run(
            ['psql', *self.connection, '-d', database, '-X', '-A', '-t', '-v', 'ON_ERROR_STOP=1'],
            input=sql,
            text=True,
            check=True,
            capture_output=True,
        ).stdout

    def dump(self, database: str, destination: Path, *options: str) -> None:
        """Выгрузить базу штатным pg_dump с заданными форматом и сжатием."""
        subprocess.run(
            [
                'pg_dump',
                *self.connection,
                '-d',
                database,
                '--no-owner',
                '--no-privileges',
                *options,
                '-f',
                str(destination),
            ],
            check=True,
            capture_output=True,
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
        subprocess.run(
            [
                'initdb',
                '-D',
                str(cluster),
                '-U',
                'fixture',
                '--auth-local=trust',
                '--auth-host=reject',
                '--no-locale',
                '--encoding=UTF8',
            ],
            check=True,
            capture_output=True,
        )
        try:
            subprocess.run(
                [
                    'pg_ctl',
                    '-D',
                    str(cluster),
                    '-l',
                    str(root / 'postgres.log'),
                    '-o',
                    f"-F -h '' -k {root} -p 55432",
                    '-w',
                    'start',
                ],
                check=True,
                capture_output=True,
            )
            yield Postgres(root)
        finally:
            # При неудачном старте сервер мог успеть создать postmaster.pid.
            if (cluster / 'postmaster.pid').exists():
                subprocess.run(
                    ['pg_ctl', '-D', str(cluster), '-m', 'immediate', '-w', 'stop'],
                    check=True,
                    capture_output=True,
                )
