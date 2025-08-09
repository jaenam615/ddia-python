import os
import json
from chapter_3.mini_db.common.utils import pack_record, unpack_record

"""
A very simple SSTable representation:
- Each segment is a file "segment_{n}.sst" in provided dir.
- Format: newline-delimited JSON index at start? (for simplicity we'll write binary record stream and a small JSON index file)
Approach:
 - data file: segment_{n}.data  (concatenated framed records)
 - index file: segment_{n}.idx  (json mapping key_hex -> (offset, length))
This is not space-efficient but simple and good for learning.
"""

class SSTableManager:
    def __init__(self, path: str):
        os.makedirs(path, exist_ok=True)
        self.path = path
        self._next_id = self._discover_next_id()
        self.segments: list[str] = []  # list of segment base names (without extension)
        # load existing segments
        for fname in os.listdir(self.path):
            if fname.endswith(".idx"):
                base = fname[:-4]
                if base not in self.segments:
                    self.segments.append(base)

    def _discover_next_id(self) -> int:
        existing = [int(f.split("_")[1].split(".")[0]) for f in os.listdir(self.path) if f.startswith("segment_") and f.endswith(".data")]
        if not existing:
            return 1
        return max(existing) + 1

    def flush_memtable(self, items: list[tuple[bytes | bytes]]) -> str:
        """
        items: list of (key, value) pairs. We will sort by key and write a new segment.
        Returns base segment name.
        """
        if not items:
            return ""
        items_sorted = sorted(items, key=lambda kv: kv[0])
        seg_id = self._next_id
        self._next_id += 1
        base = f"segment_{seg_id}"
        data_path = os.path.join(self.path, base + ".data")
        idx_path = os.path.join(self.path, base + ".idx")
        idx = {}
        offset = 0
        with open(data_path, "wb") as df:
            for k, v in items_sorted:
                rec = pack_record(k, v)
                df.write(rec)
                idx[k.hex()] = (offset, len(rec))
                offset += len(rec)
        # write index as json (mapping key_hex -> [offset,length])
        with open(idx_path, "w", encoding="utf-8") as ix:
            json.dump(idx, ix)
        self.segments.insert(0, base)  # newest first for lookup
        return base

    def lookup_in_segment(self, base: str, key: bytes) -> bytes | None:
        data_path = os.path.join(self.path, base + ".data")
        idx_path = os.path.join(self.path, base + ".idx")
        if not os.path.exists(idx_path):
            return None
        with open(idx_path, "r", encoding="utf-8") as ix:
            idx = json.load(ix)
        khex = key.hex()
        if khex not in idx:
            return None
        offset, length = idx[khex]
        with open(data_path, "rb") as df:
            df.seek(offset)
            rec = df.read(length)
            k, v = unpack_record(rec)
            return v

    def lookup(self, key: bytes) -> bytes | None:
        # search segments newest -> oldest
        for base in self.segments:
            val = self.lookup_in_segment(base, key)
            if val is not None:
                return val
        return None