"""Перегенерировать реальные дампы из SQL-источников: python -m tools.generate_fixtures."""

import argparse
import re
import tempfile
from pathlib import Path

from tools.postgres import postgres_cluster, run_postgres

FIXTURES = Path(__file__).resolve().parents[1] / 'tests'


def generate(dump_format: str, expected_major: int) -> None:
    """Создать и проверить дампы до замены отслеживаемых файлов.

    Plain создаётся только pg_dump 15; custom — выбранной версией 15–18 с Z0/Z6.
    Источник — fixtures/source.sql соответствующего формата. Каждый результат
    восстанавливается в пустую БД. Ошибка любой проверки сохраняет прежние файлы;
    успешные файлы заменяются атомарно по одному в пределах той же файловой системы.
    """
    version = run_postgres('pg_dump', '--version').stdout
    match = re.search(r'(\d+)\.', version)
    if match is None or int(match[1]) != expected_major:
        message = f'Unexpected pg_dump version: {version.strip()} (expected {expected_major})'
        raise ValueError(message)
    if dump_format == 'plain' and expected_major != 15:
        message = 'The single plain snapshot requires pg_dump 15'
        raise ValueError(message)
    fixtures = FIXTURES / dump_format / 'fixtures'
    with postgres_cluster() as postgres:
        database = 'plain_fixtures' if dump_format == 'plain' else 'postgres'
        if database != 'postgres':
            postgres.create_database(database)
        postgres.sql(database, (fixtures / 'source.sql').read_text(encoding='utf-8'))
        outputs = []
        compressions = (None,) if dump_format == 'plain' else (0, 6)
        for index, compression in enumerate(compressions):
            name = (
                f'postgres{expected_major}.sql'
                if compression is None
                else f'postgres{expected_major}-z{compression}.dump'
            )
            candidate = postgres.root / name
            options = ('-Fp',) if compression is None else ('-Fc', f'-Z{compression}')
            postgres.dump(database, candidate, *options)
            verify_database = f'verify_{index}'
            postgres.create_database(verify_database)
            if compression is None:
                postgres.sql(verify_database, candidate.read_text(encoding='utf-8'))
            else:
                run_postgres(
                    'pg_restore',
                    *postgres.connection,
                    '-d',
                    verify_database,
                    '--exit-on-error',
                    str(candidate),
                )
            outputs.append((candidate, fixtures / name))
        # Сначала проверяем все результаты, затем публикуем каждый через rename.
        with tempfile.TemporaryDirectory(prefix='.generated-', dir=fixtures) as directory:
            for candidate, destination in outputs:
                staging = Path(directory) / destination.name
                staging.write_bytes(candidate.read_bytes())
                staging.replace(destination)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--format', choices=('plain', 'custom'), required=True)
    parser.add_argument('--expected-major', type=int, choices=(15, 16, 17, 18), required=True)
    args = parser.parse_args()
    generate(args.format, args.expected_major)
