from abc import ABC, abstractmethod


class ProcessingInterface(ABC):
    """
    처리 계층(OLTP/OLAP)을 위한 공통 인터페이스.
    - OLTP는 단순한 point read/write 위주
    - OLAP는 범위/집계/스캔 기능 등 확장을 예상
    """

    @abstractmethod
    def execute(self, op: str, *args, **kwargs):
        """
        op: 연산 종류 (e.g., "get", "set", "scan")
        args/kwargs: 연산별 파라미터
        """
        ...

