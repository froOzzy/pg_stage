import io

import pytest

from pg_stage.constants import Constants
from pg_stage.exceptions import PgDumpError
from pg_stage.obfuscators.custom import BufferedStreamReader, DumpIO
from tests.custom.helpers import pack_int


@pytest.mark.parametrize('value', [0, 1, -1, 255, 65536, 2147483647, -2147483648])
def test_signed_integer_encoding(value: int) -> None:
    """
    Arrange: Положительное, отрицательное или нулевое число в формате PostgreSQL
    Act: Независимое декодирование и кодирование через DumpIO
    Assert: Значение и байтовое представление совпадают с форматом PostgreSQL
    """
    assert DumpIO().read_int(io.BytesIO(pack_int(value))) == value
    assert DumpIO().write_int(value) == pack_int(value)


@pytest.mark.parametrize(
    'method, payload',
    [
        ('read_byte', b''),
        ('read_int', b'\x00\x01'),
        ('read_offset', b'\x01'),
        ('read_string', pack_int(4) + b'ab'),
    ],
)
def test_truncated_binary_input_raises(method: str, payload: bytes) -> None:
    """
    Arrange: Бинарный поток с неполным числом, смещением или строкой
    Act: Чтение соответствующего значения через DumpIO
    Assert: Выбрасывается PgDumpError вместо незаметной потери данных
    """
    with pytest.raises(PgDumpError):
        getattr(DumpIO(), method)(io.BytesIO(payload))


@pytest.mark.parametrize('value', ['', 'ASCII', 'Кириллица и emoji 🐘'])
def test_utf8_string(value: str) -> None:
    """
    Arrange: Строка UTF-8 с префиксом длины в байтах
    Act: Чтение строки через DumpIO
    Assert: Пустая строка и многобайтовые символы восстановлены без изменений
    """
    encoded = value.encode('utf-8')
    assert DumpIO().read_string(io.BytesIO(pack_int(len(encoded)) + encoded)) == value


def test_invalid_utf8_raises() -> None:
    """
    Arrange: Строка с недопустимым UTF-8
    Act: Чтение строки через DumpIO
    Assert: Выбрасывается PgDumpError с причиной ошибки кодировки
    """
    with pytest.raises(PgDumpError, match='Invalid UTF-8'):
        DumpIO().read_string(io.BytesIO(pack_int(1) + b'\xff'))


def test_buffered_reader_bypass(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Arrange: Поток с заголовком и данными, буфер меньше общего размера потока
    Act: Чтение заголовка с bypass и последующее чтение данных без bypass
    Assert: Выведены только прочитанные байты заголовка, данные прочитаны без потерь
    """
    monkeypatch.setattr(Constants, 'DEFAULT_BUFFER_SIZE', 8)
    output = io.BytesIO()
    reader = BufferedStreamReader(io.BytesIO(b'header-payload'), output)
    reader.bypass_on()
    assert reader.read(7) == b'header-'
    reader.bypass_off()
    assert reader.read(7) == b'payload'
    assert reader.read(1) == b''
    assert output.getvalue() == b'header-'


@pytest.mark.xfail(
    strict=True, raises=AssertionError, reason='read(size) ограничен двумя буферами и возвращает неполные данные'
)
def test_buffered_reader_large_read(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Arrange: Запрос чтения больше внутреннего ограничения буфера
    Act: Чтение всего запрошенного значения за один вызов
    Assert: Возвращены все байты, необходимые для чтения длинной строки TOC
    """
    monkeypatch.setattr(Constants, 'DEFAULT_BUFFER_SIZE', 8)
    data = b'x' * 33
    assert BufferedStreamReader(io.BytesIO(data), io.BytesIO()).read(len(data)) == data
