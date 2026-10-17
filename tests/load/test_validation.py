"""Быстрая регрессия валидатора нагрузки, выполняемая и без --run-load."""

import sys

import pytest

pytestmark = pytest.mark.skipif(sys.platform != 'linux', reason='Requires Linux load worker')


def test_conditions_reject_unconditional_mutation():
    """
    Arrange: Две соседние строки с истинным и ложным условием
    Act: Worker получает ошибочно обфусцированное значение в обеих строках
    Assert: Проверка отвергает вторую строку, вместо пропуска ложной ветки
    """
    from tests.load.worker import DumpInput, DumpOutput

    output = DumpOutput(DumpInput('conditions', 2000), None)
    output.write('COPY users (c0, c1, c2, c3, c4, c5) FROM stdin;\n')
    output.write('0\thidden\tyes\toriginal\t\\N\ttext\\tvalue\n')
    with pytest.raises(AssertionError, match='Conditional mutation is incorrect'):
        output.write('1\thidden\tno\toriginal\t\\N\ttext\\tvalue\n')
