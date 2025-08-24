import pytest

from chapter_3.mini_db.index.lsm_index import LSMIndex


def test_lsm_put_get_delete():
    idx = LSMIndex()
    idx.put(b"a", ("mem", None, None, None))
    idx.put(b"a", ("sst", "segment_1", 0, 10))
    assert idx.get(b"a")[0] == "sst"
    idx.delete(b"a")
    assert idx.get(b"a") is None

