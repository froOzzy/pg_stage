import pytest

from pg_stage.obfuscators.plain import PlainObfuscator
from tests.plain.helpers import PlainDump

pytest_plugins = ['tests.load.plugin']


@pytest.fixture(autouse=True)
def obfuscator_object() -> PlainObfuscator:
    return PlainObfuscator()


@pytest.fixture
def plain_dump() -> PlainDump:
    return PlainDump()
