import argparse
import os

from chapter_3.mini_db.engine.mini_db import MiniDB
from chapter_3.mini_db.index.hash_index import HashIndex
from chapter_3.mini_db.index.lsm_index import LSMIndex
from chapter_3.mini_db.index.b_tree_index import BTreeIndex


def _build_index(name: str):
    name = name.lower()
    if name == "hash":
        return HashIndex()
    if name == "lsm":
        return LSMIndex()
    if name in ("btree", "b_tree"):
        return BTreeIndex()
    raise ValueError(f"Unknown index: {name}")


def _is_ascii(s: str) -> bool:
    try:
        s.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def repl(db: MiniDB):
    print("Commands: set <key> <value> | get <key> | flush | compact | help | quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break
        if not raw:
            continue
        parts = raw.split()
        cmd = parts[0].lower()
        if cmd in ("quit", "exit"):  # quit
            break
        if cmd == "help":
            print("Commands: set <key> <value> | get <key> | flush | compact | help | quit")
            continue
        if cmd == "set":
            if len(parts) < 3:
                print("Usage: set <key> <value>")
                continue
            key, value = parts[1], " ".join(parts[2:])
            if not _is_ascii(key) or not _is_ascii(value):
                print("Error: key/value must be ASCII-only")
                continue
            db.db_set(key, value.encode("ascii"))
            print("OK")
            continue
        if cmd == "get":
            if len(parts) != 2:
                print("Usage: get <key>")
                continue
            key = parts[1]
            if not _is_ascii(key):
                print("Error: key must be ASCII-only")
                continue
            val = db.db_get(key)
            if val is None:
                print("(nil)")
            else:
                try:
                    print(val.decode("ascii"))
                except UnicodeDecodeError:
                    print(val)
            continue
        if cmd == "flush":
            db.flush()
            print("Flushed")
            continue
        if cmd == "compact":
            db.compact()
            print("Compacted")
            continue
        print("Unknown command. Type 'help' for commands.")


def main():
    parser = argparse.ArgumentParser(description="MiniDB interactive CLI")
    parser.add_argument("--index", choices=["hash", "lsm", "btree"], default="hash")
    parser.add_argument("--data-dir", default=os.environ.get("MINIDB_DATA_DIR", "/tmp/mini_db_cli"))
    parser.add_argument("--mem-threshold", type=int, default=256)
    args = parser.parse_args()

    os.makedirs(args.data_dir, exist_ok=True)
    index_impl = _build_index(args.index)
    db = MiniDB(data_dir=args.data_dir, mem_threshold=args.mem_threshold, index=index_impl)

    print("=== MiniDB CLI ===")
    print(f"Index: {args.index} | DataDir: {args.data_dir} | MemThreshold: {args.mem_threshold}")
    try:
        repl(db)
    finally:
        db.close()
        print("Closed.")


if __name__ == "__main__":
    main()