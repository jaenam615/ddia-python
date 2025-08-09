import os
from chapter_3.mini_db.storage.wal import WAL
from chapter_3.mini_db.storage.memtable import MemTable
from chapter_3.mini_db.storage.ss_table import SSTableManager
from chapter_3.mini_db.index.hash_index import HashIndex

DATA_ROOT_DEFAULT = "data_dir"

class MiniDB:
    """
    Minimal DB implementing:
      - WAL append for durability
      - MemTable (in-memory)
      - Flush memtable -> SSTableManager (sorted segment + index)
      - HashIndex that points to ('mem') or ('sst', base, offset, length)
    Recovery:
      - On startup, read WAL and populate memtable + index (mem entries)
      - Note: for simplicity, when flush occurs, we write SSTable and update index to point into SSTable
    """
    def __init__(self, data_dir: str | None = None, mem_threshold: int = 100):
        self.data_dir = data_dir or DATA_ROOT_DEFAULT
        os.makedirs(self.data_dir, exist_ok=True)
        self.wal = WAL(self.data_dir)
        self.mem = MemTable()
        self.sstable = SSTableManager(self.data_dir)
        self.index = HashIndex()
        self.mem_threshold = mem_threshold
        # recover WAL into memtable & index (mem-records)
        self._recover()

    def _recover(self):
        # replay WAL into memtable (newer entries override)
        for k, v in self.wal.iter_records():
            self.mem.put(k, v)
            self.index.put(k, ("mem", None, None, None))

    def db_set(self, key: str, value: bytes):
        kb = key.encode()
        # append to WAL first
        self.wal.append(kb, value)
        # put to memtable
        self.mem.put(kb, value)
        self.index.put(kb, ("mem", None, None, None))
        # flush if threshold exceeded
        if len(self.mem) >= self.mem_threshold:
            self._flush_memtable()

    def _flush_memtable(self):
        items = list(self.mem.items())
        if not items:
            return
        # flush to sstable manager (returns base)
        base = self.sstable.flush_memtable(items)
        # update index entries to point to sstable offsets (read idx file to map offsets)
        # We'll load the idx file and update index accordingly
        import json
        idx_path = os.path.join(self.data_dir, base + ".idx")
        with open(idx_path, "r", encoding="utf-8") as ix:
            idx = json.load(ix)
        for khex, (offset, length) in idx.items():
            self.index.put(bytes.fromhex(khex), ("sst", base, offset, length))
        # clear memtable and wipe WAL (simple approach)
        self.mem.clear()
        self.wal.wipe()

    def db_get(self, key: str) -> bytes | None:
        kb = key.encode()
        # check index first
        loc = self.index.get(kb)
        if loc is None:
            return None
        if loc[0] == "mem":
            return self.mem.get(kb)
        elif loc[0] == "sst":
            _, base, offset, length = loc
            # Try the pointed segment first
            val = self.sstable.lookup_in_segment(base, kb)
            if val is not None:
                return val
            # Fallback: search all segments (in case of compaction/rename later)
            return self.sstable.lookup(kb)
        else:
            return None

    def close(self):
        self.wal.close()

    def flush(self):
        self._flush_memtable()