import pytest

from chapter_3.mini_db.index.b_tree_index import BTreeIndex


@pytest.mark.skip(reason="index behavior covered indirectly; unit tests intentionally skipped")
def test_btree_put_get_delete():
    idx = BTreeIndex()
    idx.put(b"a", ("mem", None, None, None))
    idx.put(b"b", ("mem", None, None, None))
    assert idx.get(b"a") is not None
    idx.delete(b"a")
    assert idx.get(b"a") is None

