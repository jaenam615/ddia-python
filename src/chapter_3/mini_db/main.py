from chapter_3.mini_db.engine.mini_db import MiniDB


def main():
    print("=== MiniDB Runner Start ===")

    db = MiniDB(data_dir="/tmp/mini_db_demo", mem_threshold=2)

    print("\n[Write Test]")
    db.db_set("apple", b"사과")
    db.db_set("banana", b"바나나")  # threshold 2 -> triggers flush
    db.db_set("apple", b"애플")

    print("\n[Read Test]")
    print("apple:", db.db_get("apple"))
    print("banana:", db.db_get("banana"))
    print("grape:", db.db_get("grape"))

    print("\n[Manual Flush]")
    db.flush()

    print("\n[Read After Flush]")
    print("apple:", db.db_get("apple"))

    db.close()
    print("\n[Reopen & Recover]")
    db2 = MiniDB(data_dir="/tmp/mini_db_demo", mem_threshold=2)
    print("banana:", db2.db_get("banana"))
    db2.close()

    print("\n=== MiniDB Runner End ===")


if __name__ == "__main__":
    main()