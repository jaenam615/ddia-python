from chapter_3.mini_db.engine.mini_db import MiniDB
from chapter_3.mini_db.index.hash_index import HashIndex
from chapter_3.mini_db.index.b_tree_index import BTreeIndex
from chapter_3.mini_db.index.lsm_index import LSMIndex


def _smoke(db: MiniDB):
    db.db_set("a", b"1")
    db.db_set("b", b"2")
    assert db.db_get("a") == b"1"
    db.flush()
    assert db.db_get("b") == b"2"
    db.compact()
    assert db.db_get("a") == b"1"
    db.close()


def test_engine_with_hash(tmp_path):
    db = MiniDB(data_dir=str(tmp_path / "hash"), mem_threshold=2, index=HashIndex())
    _smoke(db)


def test_engine_with_btree(tmp_path):
    db = MiniDB(data_dir=str(tmp_path / "btree"), mem_threshold=2, index=BTreeIndex())
    _smoke(db)


def test_engine_with_lsm(tmp_path):
    db = MiniDB(data_dir=str(tmp_path / "lsm"), mem_threshold=2, index=LSMIndex())
    _smoke(db)

