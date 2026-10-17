"""Независимое кодирование тестовых чанков custom-формата без DumpIO проекта."""

import io
import zlib


def pack_int(value: int) -> bytes:
    return bytes([int(value < 0)]) + abs(value).to_bytes(4, 'little')


def pack_chunks(payload: bytes, *, compressed: bool, chunk_size: int = 11) -> bytes:
    data = zlib.compress(payload) if compressed else payload
    return b''.join(
        pack_int(len(data[index : index + chunk_size])) + data[index : index + chunk_size]
        for index in range(0, len(data), chunk_size)
    ) + pack_int(0)


def unpack_block(data: bytes, *, compressed: bool) -> tuple[int, bytes]:
    stream = io.BytesIO(data)
    block = read_block(stream, compressed=compressed)
    assert stream.read() == b'', 'Unexpected bytes after zero terminator'
    return block


def read_block(stream: io.BytesIO, *, compressed: bool) -> tuple[int, bytes]:
    assert stream.read(1) == b'\x01'

    def read_int() -> int:
        encoded = stream.read(5)
        assert len(encoded) == 5, 'Missing chunk length or zero terminator'
        return int.from_bytes(encoded[1:], 'little') * (-1 if encoded[0] else 1)

    dump_id = read_int()
    chunks = []
    while True:
        size = read_int()
        if size == 0:
            break
        assert size > 0
        chunk = stream.read(size)
        assert len(chunk) == size, 'Truncated output chunk'
        chunks.append(chunk)
    payload = b''.join(chunks)
    return dump_id, zlib.decompress(payload) if compressed else payload
