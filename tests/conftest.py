import pytest

from pg_stage.obfuscators.plain import PlainObfuscator


@pytest.fixture(autouse=True)
def obfuscator_object() -> PlainObfuscator:
    return PlainObfuscator()
