from chapter_3.mini_db.interfaces.storage_engine_interface import StorageEngine


class DummyEngine(StorageEngine):
    def __init__(self):
        self._d = {}

    def put(self, key: bytes, value: bytes) -> None:
        self._d[key] = value

    def get(self, key: bytes) -> bytes | None:
        return self._d.get(key)

    def flush(self):
        pass


def test_storage_engine_interface_contract():
    e = DummyEngine()
    e.put(b"a", b"1")
    assert e.get(b"a") == b"1"

