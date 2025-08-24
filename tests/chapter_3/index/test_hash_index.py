from chapter_3.mini_db.index.hash_index import HashIndex


def test_hash_index_put_get_delete():
    idx = HashIndex()
    idx.put(b"a", ("mem", None, None, None))
    assert idx.get(b"a")[0] == "mem"
    idx.delete(b"a")
    assert idx.get(b"a") is None

