from abc import ABC, abstractmethod

class StorageEngine(ABC):
    @abstractmethod
    def put(self, key: bytes, value: bytes) -> None: ...

    @abstractmethod
    def get(self, key: bytes) -> bytes | None: ...

    @abstractmethod
    def flush(self): ...