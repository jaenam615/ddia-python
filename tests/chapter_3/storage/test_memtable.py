from chapter_3.mini_db.storage.memtable import MemTable


def test_memtable_basic():
    m = MemTable()
    m.put(b"a", b"1")
    m.put(b"b", b"2")
    assert m.get(b"a") == b"1"
    assert len(m) == 2
    m.clear()
    assert len(m) == 0

