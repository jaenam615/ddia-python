import random
import string
from typing import Iterable, List, Tuple


ASCII_ALPHANUM = string.ascii_letters + string.digits


def generate_kv_pairs(
    count: int,
    key_prefix: str = "key",
    key_width: int = 6,
    value_len: int = 64,
    seed: int | None = 42,
) -> List[Tuple[str, bytes]]:
    """
    Generate deterministic ASCII-only keys/values suitable for benchmarking.
    - Keys: f"{key_prefix}{i:0{key_width}d}" for i in [0, count)
    - Values: random ASCII alphanumerics of length `value_len` (seeded)
    Returns list of (key_str, value_bytes)
    """
    if seed is not None:
        random.seed(seed)
    values: List[bytes] = []
    for _ in range(count):
        s = "".join(random.choice(ASCII_ALPHANUM) for _ in range(value_len))
        values.append(s.encode("ascii"))
    items: List[Tuple[str, bytes]] = []
    for i in range(count):
        k = f"{key_prefix}{i:0{key_width}d}"
        items.append((k, values[i]))
    return items


def shuffle_keys(keys: List[str], seed: int | None = 123) -> List[str]:
    ks = list(keys)
    if seed is not None:
        random.seed(seed)
    random.shuffle(ks)
    return ks

