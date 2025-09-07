import hashlib

from chatper_6.partition_interface import PartitionInterface


class HashPartition(PartitionInterface):
    def __init__(self, nodes: list[str]):
        self.nodes = nodes

    def get_node(self, key: str) -> str:
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return self.nodes[h % len(self.nodes)]