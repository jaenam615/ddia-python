import time
import os
import shutil
from dataclasses import dataclass
from typing import Callable, List, Tuple

from chapter_3.mini_db.engine.mini_db import MiniDB
from chapter_3.mini_db.index.hash_index import HashIndex
from chapter_3.mini_db.index.lsm_index import LSMIndex
from chapter_3.mini_db.index.b_tree_index import BTreeIndex
from chapter_3.mini_db.bench.workload import generate_kv_pairs, shuffle_keys


@dataclass
class BenchResult:
    index_name: str
    num_items: int
    set_total_s: float
    set_ops_per_s: float
    get_total_s: float
    get_ops_per_s: float


def _time_op(fn: Callable[[], None]) -> float:
    t0 = time.perf_counter()
    fn()
    t1 = time.perf_counter()
    return t1 - t0


def wipe_dir(path: str) -> None:
    """Remove a directory tree if it exists (used to reset bench data)."""
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)


def bench_index(
    index_ctor: Callable[[], object],
    data_dir: str,
    num_items: int = 1000,
    mem_threshold: int = 256,
    clean_before: bool = False,
    clean_after: bool = False,
) -> BenchResult:
    if clean_before:
        wipe_dir(data_dir)
    items = generate_kv_pairs(num_items)

    db = MiniDB(data_dir=data_dir, mem_threshold=mem_threshold, index=index_ctor())

    # SET phase
    def do_sets():
        for k, v in items:
            db.db_set(k, v)
        db.flush()

    set_total = _time_op(do_sets)
    set_ops_per_s = num_items / set_total if set_total > 0 else float("inf")

    # GET phase (random order)
    keys = [k for k, _ in items]
    keys = shuffle_keys(keys)

    def do_gets():
        for k in keys:
            _ = db.db_get(k)

    get_total = _time_op(do_gets)
    get_ops_per_s = num_items / get_total if get_total > 0 else float("inf")

    # finalize
    db.close()
    if clean_after:
        wipe_dir(data_dir)

    return BenchResult(
        index_name=index_ctor.__name__,
        num_items=num_items,
        set_total_s=set_total,
        set_ops_per_s=set_ops_per_s,
        get_total_s=get_total,
        get_ops_per_s=get_ops_per_s,
    )


def run_all(
    data_root: str = "/tmp/mini_db_bench",
    num_items: int = 10000,
    clean_before_each: bool = False,
    clean_after_each: bool = False,
) -> List[BenchResult]:
    configs = [
        (HashIndex, f"{data_root}_hash"),
        (LSMIndex, f"{data_root}_lsm"),
        (BTreeIndex, f"{data_root}_btree"),
    ]
    results: List[BenchResult] = []
    for ctor, dir_ in configs:
        results.append(
            bench_index(
                ctor,
                dir_,
                num_items=num_items,
                clean_before=clean_before_each,
                clean_after=clean_after_each,
            )
        )
    return results


def print_results(results: List[BenchResult]) -> None:
    print("Index, Items, SetTotal(s), SetOps/s, GetTotal(s), GetOps/s")
    for r in results:
        print(
            f"{r.index_name}, {r.num_items}, "
            f"{r.set_total_s:.6f}, {r.set_ops_per_s:.1f}, "
            f"{r.get_total_s:.6f}, {r.get_ops_per_s:.1f}"
        )


def main():
    res = run_all()
    print_results(res)


if __name__ == "__main__":
    main()

