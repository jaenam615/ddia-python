import hashlib

from chatper_6.partition_interface import PartitionInterface


class RangePartition(PartitionInterface):
    def __init__(self, ranges: list[tuple[int, str]]):
        """
        Example: [(333333, "node1"), (666666, "node2"), (999999, "node3")]
        """
        self.ranges = ranges

    def get_node(self, key: str) -> str:
        h = int(hashlib.md5(key.encode()).hexdigest(), 16) % 1000000
        for upper, node in self.ranges:
            if h <= upper:
                return node