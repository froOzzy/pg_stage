"""Общие pytest-фикстуры и опции обязательных интеграционных проверок."""

import shutil

import pytest

from tests.tools.postgres import postgres_cluster

pytest_plugins = ['tests.load.plugin']


def pytest_addoption(parser):
    """Разрешить CI требовать PostgreSQL вместо пропуска интеграционных проверок."""
    parser.addoption('--require-postgres', action='store_true', help='Fail if PostgreSQL tools are unavailable')


@pytest.fixture(scope='session')
def postgres(request):
    """Запустить один временный кластер; локально пропустить тест при отсутствии утилит."""
    missing = [name for name in ('initdb', 'pg_ctl', 'psql', 'createdb') if shutil.which(name) is None]
    if missing:
        message = 'Missing PostgreSQL tools: ' + ', '.join(missing)
        if request.config.getoption('--require-postgres'):
            pytest.fail(message)
        pytest.skip(message)
    with postgres_cluster() as cluster:
        yield cluster
