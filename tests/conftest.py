import pytest

from src.pg_stage.obfuscator import Obfuscator


@pytest.fixture(autouse=True)
def obfuscator_object():
    return Obfuscator()
