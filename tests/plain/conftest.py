"""Pytest-фикстуры plain-обфускатора и сценариев сохранённого дампа."""

import pytest

from pg_stage.obfuscators.plain import PlainObfuscator
from tests.plain.helpers import PlainDump


@pytest.fixture
def obfuscator_object() -> PlainObfuscator:
    """Создать новый plain-обфускатор без состояния предыдущего теста."""
    return PlainObfuscator()


@pytest.fixture
def plain_dump() -> PlainDump:
    """Предоставить доступ к сценариям единственного сохранённого plain-дампа."""
    return PlainDump()
