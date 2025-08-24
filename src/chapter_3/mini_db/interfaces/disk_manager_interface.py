from abc import ABC, abstractmethod

class DiskManagerInterface(ABC):
    @abstractmethod
    def read_page(self, page_id: int) -> bytes: ...

    @abstractmethod
    def write_page(self, page_id: int, data: bytes): ...

    @abstractmethod
    def alloc_page(self) -> int: ...
