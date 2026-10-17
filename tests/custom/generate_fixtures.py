"""Создать custom-дампы PostgreSQL 15–18 в изолированном временном кластере."""

import argparse
import re
import subprocess
import tempfile
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / 'fixtures'


def generate(expected_major=None):
    version = subprocess.check_output(['pg_dump', '--version'], text=True)
    match = re.search(r'(\d+)\.', version)
    major = int(match.group(1)) if match else None
    if major not in (15, 16, 17, 18) or (expected_major is not None and major != expected_major):
        message = f'Unexpected pg_dump version: {version.strip()} (expected major: {expected_major})'
        raise ValueError(message)
    with tempfile.TemporaryDirectory(prefix='pg-stage-fixtures-') as directory:
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
        connection = ['-h', str(root), '-p', '55432', '-U', 'fixture', '-d', 'postgres']
        try:
            subprocess.run(
                ['psql', *connection, '-v', 'ON_ERROR_STOP=1', '-f', str(FIXTURES / 'source.sql')],
                check=True,
                capture_output=True,
            )
            for compression in (0, 6):
                subprocess.run(
                    [
                        'pg_dump',
                        *connection,
                        '-Fc',
                        f'-Z{compression}',
                        '--no-owner',
                        '--no-privileges',
                        '-f',
                        str(FIXTURES / f'postgres{major}-z{compression}.dump'),
                    ],
                    check=True,
                )
        finally:
            subprocess.run(['pg_ctl', '-D', str(cluster), '-m', 'immediate', '-w', 'stop'], check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-major', type=int, choices=(15, 16, 17, 18))
    generate(parser.parse_args().expected_major)
