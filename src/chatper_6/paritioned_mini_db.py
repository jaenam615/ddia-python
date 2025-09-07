from chapter_3.mini_db.engine.mini_db import MiniDB
from chapter_3.mini_db.interfaces.index_interface import IndexInterface
from chatper_6.partition_interface import PartitionInterface


class PartitionedMiniDB:
    def __init__(self, partitioner: PartitionInterface, nodes: list[str], mem_threshold=100):
        self.partitioner = partitioner
        self.nodes = nodes
        self.node_dbs = {node: MiniDB(mem_threshold=mem_threshold) for node in nodes}

    def set(self, key: str, value: bytes):
        node = self.partitioner.get_node(key)
        db = self.node_dbs[node]
        db.db_set(key, value)
        print(f"Set {key} -> {value} in {node}")

    def get(self, key: str) -> bytes | None:
        node = self.partitioner.get_node(key)
        db = self.node_dbs[node]
        return db.db_get(key)

    def flush_all(self):
        for db in self.node_dbs.values():
            db.flush()

    def close_all(self):
        for db in self.node_dbs.values():
            db.close()