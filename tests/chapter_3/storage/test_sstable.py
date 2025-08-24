import os

from chapter_3.mini_db.storage.ss_table import SSTableManager


def test_sstable_flush_and_lookup(tmp_path):
    mgr = SSTableManager(str(tmp_path))
    base = mgr.flush_memtable([(b"a", b"1"), (b"b", b"2")])
    assert base
    assert mgr.lookup_in_segment(base, b"a") == b"1"
    # lookup across segments API
    assert mgr.lookup(b"b") == b"2"

