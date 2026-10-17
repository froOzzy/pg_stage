"""Граница выполнения внешних PostgreSQL-команд."""

import json
import os
import sys

import pytest

from tools.postgres import run_postgres


def test_unknown_executable_is_rejected():
    """
    Arrange: Имя командной оболочки вместо разрешённой PostgreSQL-утилиты
    Act: Попытка выполнить команду через общий runner
    Assert: Получен ValueError до запуска внешнего процесса
    """
    with pytest.raises(ValueError, match='Unsupported PostgreSQL tool'):
        run_postgres('sh', '-c', 'exit 0')


def test_missing_executable_is_reported(monkeypatch):
    """
    Arrange: PATH не содержит установленных PostgreSQL-утилит
    Act: Запуск pg_dump через общий runner
    Assert: Ошибка явно сообщает об отсутствующей утилите
    """
    monkeypatch.setenv('PATH', '')
    with pytest.raises(FileNotFoundError, match='PostgreSQL tool not found in PATH: pg_dump'):
        run_postgres('pg_dump', '--version')


@pytest.mark.skipif(os.name != 'posix', reason='Requires executable script support')
def test_arguments_are_passed_literally(tmp_path, monkeypatch):
    """
    Arrange: Тестовый pg_dump и аргумент с пробелами, кавычками и shell-подстановкой
    Act: Запуск runner с относительной записью PATH из другого рабочего каталога
    Assert: executable разрешён в абсолютный путь, аргумент передан целиком, shell не исполнялся
    """
    binary_directory = tmp_path / 'bin'
    binary_directory.mkdir()
    executable = binary_directory / 'pg_dump'
    executable.write_text(f'#!{sys.executable}\nimport json, sys\nprint(json.dumps(sys.argv))\n', encoding='utf-8')
    executable.chmod(0o700)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('PATH', 'bin')
    marker = tmp_path / 'shell-executed'
    argument = f"value with spaces ' ; $(touch {marker})"

    result = run_postgres('pg_dump', argument)

    assert json.loads(result.stdout) == [str(executable.resolve()), argument]
    assert not marker.exists()
