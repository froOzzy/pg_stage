import pytest

from pg_stage.obfuscators.plain import PlainObfuscator
from tests.plain.helpers import PlainDumps

pytest_plugins = ['tests.load.plugin']


@pytest.fixture(autouse=True)
def obfuscator_object() -> PlainObfuscator:
    return PlainObfuscator()


@pytest.fixture(params=(15, 16, 17, 18), ids=lambda major: f'pg{major}')
def plain_dump(request) -> PlainDumps:
    return PlainDumps(request.param)
