# mini_db/storage/wal.py
import os
from chapter_3.mini_db.common.utils import pack_record, unpack_record

class WAL:
    """
    Very simple append-only WAL.
    Each entry: record bytes (already framed)
    We also prefix with 4-byte length for easier scanning.
    """
    def __init__(self, path: str):
        os.makedirs(path, exist_ok=True)
        self.path = os.path.join(path, "wal.log")
        # ensure file exists
        open(self.path, "ab").close()
        self._f = open(self.path, "ab")

    def append(self, key: bytes, value: bytes) -> None:
        rec = pack_record(key, value)
        llen = len(rec).to_bytes(4, "big")
        self._f.write(llen + rec)
        self._f.flush()
        os.fsync(self._f.fileno())

    def close(self):
        self._f.close()

    def iter_records(self):
        """Yield (key, value) by scanning wal.log from start."""
        with open(self.path, "rb") as f:
            while True:
                llen_b = f.read(4)
                if not llen_b:
                    break
                llen = int.from_bytes(llen_b, "big")
                rec = f.read(llen)
                if len(rec) < llen:
                    break
                # unpack record framing
                key, val = unpack_record(rec)
                yield key, val

    def wipe(self):
        """Dangerous: remove WAL (used in tests)"""
        self.close()
        os.remove(self.path)
        open(self.path, "ab").close()
        self._f = open(self.path, "ab")