from chatper_6.hash_partition import HashPartition
from chatper_6.paritioned_mini_db import PartitionedMiniDB



if __name__ == "__main__":
    nodes = ["node1", "node2", "node3"]
    partitioner = HashPartition(nodes)

    db = PartitionedMiniDB(partitioner, nodes)

    for i in range(10):
        key = f"user{i}"
        db.set(key, f"data_for_{key}".encode())

    db.flush_all()

    print(db.get("user5"))