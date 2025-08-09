
class MemTable:
    """
    Simple in-memory key->value map.
    Optionally track approximate size for flush threshold.
    """
    def __init__(self):
        self._d: dict[bytes, bytes] = {}

    def put(self, key: bytes, value: bytes):
        self._d[key] = value

    def get(self, key: bytes) -> bytes | None:
        return self._d.get(key)

    def items(self):
        return self._d.items()

    def clear(self):
        self._d.clear()

    def __len__(self):
        return len(self._d)