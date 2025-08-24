import math
import json
import hashlib
from typing import Iterable


class BloomFilter:
    """
    Minimal Bloom filter implementation backed by a bytearray.
    - Build with target false-positive rate p (default ~1%).
    - Uses double hashing over SHA-256/SHA1 digests.
    - Serialized as JSON: {"m": int, "k": int, "bits": hex-string}
    """

    def __init__(self, m_bits: int, k_hashes: int, bits: bytearray | None = None):
        if m_bits <= 0:
            raise ValueError("m_bits must be > 0")
        if k_hashes <= 0:
            raise ValueError("k_hashes must be > 0")
        self.m = m_bits
        self.k = k_hashes
        num_bytes = (m_bits + 7) // 8
        self.bits = bits if bits is not None else bytearray(num_bytes)

    @staticmethod
    def _optimal_parameters(num_items: int, false_positive_rate: float = 0.01) -> tuple[int, int]:
        if num_items <= 0:
            # default small filter
            return 1024, 2
        p = max(min(false_positive_rate, 0.5), 1e-9)
        ln2 = math.log(2)
        m = int(math.ceil(-(num_items * math.log(p)) / (ln2 ** 2)))
        k = max(1, int(round((m / num_items) * ln2)))
        # round m up to multiple of 8 for byte alignment
        m_rounded = int(math.ceil(m / 8.0) * 8)
        return m_rounded, k

    @classmethod
    def from_keys(cls, keys: Iterable[bytes], false_positive_rate: float = 0.01) -> "BloomFilter":
        keys_list = list(keys)
        m, k = cls._optimal_parameters(len(keys_list), false_positive_rate)
        bf = cls(m, k)
        for key in keys_list:
            bf.add(key)
        return bf

    def _positions(self, data: bytes):
        # double hashing using two 64-bit chunks from digests
        h1 = int.from_bytes(hashlib.sha256(data).digest()[:8], "big", signed=False)
        h2 = int.from_bytes(hashlib.sha1(data).digest()[:8], "big", signed=False)
        for i in range(self.k):
            yield (h1 + i * h2) % self.m

    def add(self, data: bytes) -> None:
        for pos in self._positions(data):
            byte_index = pos // 8
            bit_index = pos % 8
            self.bits[byte_index] |= (1 << bit_index)

    def might_contain(self, data: bytes) -> bool:
        for pos in self._positions(data):
            byte_index = pos // 8
            bit_index = pos % 8
            if (self.bits[byte_index] >> bit_index) & 1 == 0:
                return False
        return True

    def save_json(self, path: str) -> None:
        payload = {
            "m": self.m,
            "k": self.k,
            "bits": self.bits.hex(),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f)

    @classmethod
    def load_json(cls, path: str) -> "BloomFilter":
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        bits = bytearray(bytes.fromhex(payload["bits"]))
        return cls(int(payload["m"]), int(payload["k"]), bits)

