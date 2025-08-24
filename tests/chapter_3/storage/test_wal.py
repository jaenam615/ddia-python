from unittest.mock import patch

from chapter_3.mini_db.storage.wal import WAL


def test_wal_append_and_iter(tmp_path):
    wal = WAL(str(tmp_path))
    wal.append(b"a", b"1")
    wal.append(b"b", b"2")
    wal.close()

    wal2 = WAL(str(tmp_path))
    items = list(wal2.iter_records())
    assert items == [(b"a", b"1"), (b"b", b"2")]
    wal2.close()


def test_wal_wipe(tmp_path):
    wal = WAL(str(tmp_path))
    wal.append(b"x", b"y")
    wal.wipe()
    # after wipe, file exists but empty
    items = list(wal.iter_records())
    assert items == []

