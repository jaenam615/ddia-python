from abc import ABC, abstractmethod

class IndexInterface(ABC):
    @abstractmethod
    def put(self, key: bytes, loc: tuple) -> None: ...

    @abstractmethod
    def get(self, key: bytes) -> tuple | None: ...

    @abstractmethod
    def delete(self, key: bytes) -> None: ...