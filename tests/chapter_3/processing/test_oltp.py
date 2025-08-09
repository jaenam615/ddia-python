import pytest

from chapter_3.mini_db.processing.oltp import OLTPProcessor
from chapter_3.mini_db.engine.mini_db import MiniDB


@pytest.mark.skip(reason="processing behavior intentionally skipped in unit tests")
def test_oltp_execute():
    db = MiniDB(data_dir="/tmp/mini_db_test", mem_threshold=100)
    p = OLTPProcessor(db)
    p.execute("set", key="x", value=b"1")
    assert p.execute("get", key="x") == b"1"
    p.execute("flush")
    p.execute("compact")
    db.close()

