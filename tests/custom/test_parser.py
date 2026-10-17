import pytest

from pg_stage.obfuscators.custom import PgStageParser


@pytest.mark.parametrize('chunk_size', [1, 2, 7, 100])
def test_parser_handles_chunk_and_utf8_boundaries(chunk_size: int) -> None:
    """
    Arrange: Несколько строк UTF-8, пустая строка и последняя строка без перевода строки
    Act: Передача байтов чанками, в том числе с разрывом многобайтового символа, затем flush
    Assert: Каждая строка обработана отдельно, символы и границы строк сохранены
    """
    seen = []

    def parse(*, line: str) -> str:
        """Передать строку тестовому обработчику для проверки контракта адаптера."""
        seen.append(line)
        return line.upper()

    parser = PgStageParser(parse)
    data = 'Алиса\t🐘\n\nБорис\nхвост'.encode('utf-8')
    result = b''.join(parser.parse(data[index : index + chunk_size]) for index in range(0, len(data), chunk_size))
    result += parser.flush()
    assert result == 'АЛИСА\t🐘\n\nБОРИС\nХВОСТ'.encode('utf-8')
    assert seen == ['Алиса\t🐘', 'Борис', 'хвост']
    assert parser.flush() == b''


@pytest.mark.parametrize('newline', [b'\n', b''])
@pytest.mark.xfail(
    strict=True, raises=AssertionError, reason='PgStageParser сохраняет исходные байты при результате None'
)
def test_parser_drops_deleted_rows(newline: bytes) -> None:
    """
    Arrange: Обработчик возвращает None для удаляемой строки
    Act: Обработка строки с переводом строки или остатка через flush
    Assert: Удалённая строка отсутствует в выходных байтах
    """
    parser = PgStageParser(lambda *, line: None)
    assert parser.parse(b'private' + newline) + parser.flush() == b''
