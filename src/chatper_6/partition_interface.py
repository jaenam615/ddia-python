from abc import ABC, abstractmethod

class PartitionInterface(ABC):
    @abstractmethod
    def get_node(self, key: str) -> str:
        """Return the node responsible for the given key"""
        pass