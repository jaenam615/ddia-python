import os
import shutil

from chapter_3.mini_db.engine.mini_db import MiniDB


def test_put_get_and_flush(tmp_path):
    data_dir = os.path.join(tmp_path, "dbdata")
    db = MiniDB(data_dir=data_dir, mem_threshold=3)

    db.db_set("k1", b"v1")
    db.db_set("k2", b"v2")
    assert db.db_get("k1") == b"v1"
    assert db.db_get("k2") == b"v2"

    # trigger flush
    db.flush()
    assert db.db_get("k1") == b"v1"
    db.close()

    # reopen and ensure recovery from existing files
    db2 = MiniDB(data_dir=data_dir, mem_threshold=3)
    assert db2.db_get("k2") == b"v2"
    db2.close()

