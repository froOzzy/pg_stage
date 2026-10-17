"""Опции запуска и отчёт нагрузочных тестов."""

import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Optional

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def positive_int(value: str) -> int:
    """Разобрать положительное целое значение CLI; иначе вызвать ValueError."""
    number = int(value)
    if number < 1:
        message = 'Expected a positive integer'
        raise ValueError(message)
    return number


def nonnegative_float(value: str) -> float:
    """Разобрать конечный неотрицательный порог CLI; исключить NaN и бесконечность."""
    number = float(value)
    if not 0 <= number < float('inf'):
        message = 'Expected a finite nonnegative number'
        raise ValueError(message)
    return number


def pytest_addoption(parser: pytest.Parser) -> None:
    """Зарегистрировать параметры нагрузки, отчёта и необязательные пороги ресурсов."""
    group = parser.getgroup('pg-stage load tests')
    group.addoption('--run-load', action='store_true', help='Enable isolated Linux load tests')
    group.addoption('--load-rows', type=positive_int, default=100000, help='Rows per table')
    group.addoption('--load-repeats', type=positive_int, default=3, help='Fresh processes per scenario and output mode')
    group.addoption('--load-output-mode', choices=('both', 'discard', 'file'), default='both')
    group.addoption('--load-report', default='load-results.json', help='JSON report path')
    group.addoption('--load-tmp-dir', default=None, help='Filesystem directory for temporary output files')
    group.addoption('--load-timeout', type=positive_int, default=120, help='Timeout per subprocess in seconds')
    group.addoption('--load-min-rows-per-second', type=nonnegative_float, default=None)
    group.addoption('--load-max-rss-mib', type=nonnegative_float, default=None)
    group.addoption('--load-max-write-mib', type=nonnegative_float, default=None)


def pytest_configure(config: pytest.Config) -> None:
    """Зарегистрировать marker явного запуска Linux-нагрузки."""
    config.addinivalue_line('markers', 'load: isolated Linux performance and resource measurements')


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Пропустить нагрузку без --run-load и на системах без Linux /proc."""
    for item in items:
        if 'load' not in item.keywords:
            continue
        if not config.getoption('--run-load'):
            item.add_marker(pytest.mark.skip(reason='Enable with --run-load'))
        elif sys.platform != 'linux':
            item.add_marker(pytest.mark.skip(reason='Requires Linux /proc metrics'))


@pytest.fixture(scope='session')
def load_results(request):
    """Сохранить отдельные замеры и сводные показатели, в том числе при падении пороговых проверок."""
    config = request.config
    results = []
    yield results
    if not results:
        return
    summaries = []
    successful = [
        result
        for result in results
        if result.get('status') == 'passed' and result.get('measurement') != 'memory_scaling'
    ]
    for scenario, mode in sorted({(result['scenario'], result['output_mode']) for result in successful}):
        runs = [result for result in successful if result['scenario'] == scenario and result['output_mode'] == mode]
        summaries.append(
            {
                'scenario': scenario,
                'output_mode': mode,
                'runs': len(runs),
                'median_rows_per_second': median(run['rows_per_second'] for run in runs),
                'median_wall_seconds': median(run['wall_seconds'] for run in runs),
                'max_peak_rss_mib': max(run['peak_rss_mib'] for run in runs),
                'max_write_bytes': max(run['io']['write_bytes'] for run in runs),
                'max_read_bytes': max(run['io']['read_bytes'] for run in runs),
            }
        )
    commit, dirty = git_metadata()
    report = {
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'environment': {
            'python': sys.version,
            'platform': platform.platform(),
            'git_commit': commit,
            'git_dirty': dirty,
        },
        'options': {
            name: config.getoption(name)
            for name in (
                '--load-rows',
                '--load-repeats',
                '--load-output-mode',
                '--load-tmp-dir',
                '--load-timeout',
                '--load-min-rows-per-second',
                '--load-max-rss-mib',
                '--load-max-write-mib',
            )
        },
        'summaries': summaries,
        'runs': results,
    }
    report_path = Path(config.getoption('--load-report')).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    terminal = config.pluginmanager.getplugin('terminalreporter')
    if terminal:
        terminal.write_sep('-', f'Load report: {report_path}')
        for summary in summaries:
            terminal.write_line(
                f'{summary["scenario"]:14} {summary["output_mode"]:7} '
                f'{summary["median_rows_per_second"]:10,.0f} rows/s  '
                f'peak RSS {summary["max_peak_rss_mib"]:.1f} MiB  '
                f'disk write {summary["max_write_bytes"] / 1024**2:.1f} MiB'
            )


def git_metadata() -> tuple[Optional[str], Optional[bool]]:
    """Вернуть commit/dirty или None для исходников вне Git, не теряя отчёт нагрузки."""
    if shutil.which('git') is None:
        return None, None
    commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=PROJECT_ROOT, text=True, capture_output=True)
    if commit.returncode:
        return None, None
    status = subprocess.run(['git', 'status', '--porcelain'], cwd=PROJECT_ROOT, text=True, capture_output=True)
    return commit.stdout.strip(), bool(status.stdout) if status.returncode == 0 else None
