import re
import shutil
import subprocess
from pathlib import Path

import pytest

from pg_stage.constants import Constants


@pytest.fixture(autouse=True)
def custom_temp_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Изолировать временные файлы бинарного обработчика от рабочих файлов проекта."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Constants, 'DEFAULT_TMP_DIR', str(tmp_path))


@pytest.fixture
def custom_fixtures() -> Path:
    return Path(__file__).resolve().parent / 'fixtures'


@pytest.fixture
def pg_restore() -> str:
    executable = shutil.which('pg_restore')
    if executable is None:
        pytest.skip('Для независимой проверки нужен pg_restore версии 17 или новее')
    version = subprocess.check_output([executable, '--version'], text=True)
    major = re.search(r'(\d+)\.', version)
    if major is None or int(major.group(1)) < 17:
        pytest.skip(f'Нужен pg_restore >= 17, найден {version.strip()}')
    return executable
