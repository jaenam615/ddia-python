from chapter_3.mini_db.interfaces.index_interface import IndexInterface

# Location convention:
# ('mem', None, None, None)  -> value is in memtable
# ('sst', base, offset, length) -> value in segment file

class HashIndex(IndexInterface):
    def __init__(self):
        self._idx = {}  # key_hex -> location tuple

    def put(self, key: bytes, loc: tuple):
        self._idx[key.hex()] = loc

    def get(self, key: bytes) -> tuple | None:
        return self._idx.get(key.hex())

    def delete(self, key: bytes) -> None:
        self._idx.pop(key.hex(), None)