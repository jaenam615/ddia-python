from chapter_3.mini_db.interfaces.processing_interface import ProcessingInterface
from chapter_3.mini_db.engine.mini_db import MiniDB


class OLTPProcessor(ProcessingInterface):
    """
    매우 단순한 OLTP 처리기:
    - set/get/flush/compact 동작을 MiniDB에 위임
    - 향후 OLAPProcessor에서는 scan, aggregation 등을 추가할 수 있음
    """

    def __init__(self, db: MiniDB):
        self.db = db

    def execute(self, op: str, *args, **kwargs):
        if op == "set":
            key: str = kwargs["key"] if "key" in kwargs else args[0]
            value: bytes = kwargs["value"] if "value" in kwargs else args[1]
            self.db.db_set(key, value)
            return None
        if op == "get":
            key: str = kwargs["key"] if "key" in kwargs else args[0]
            return self.db.db_get(key)
        if op == "flush":
            self.db.flush()
            return None
        if op == "compact":
            self.db.compact()
            return None
        raise ValueError(f"Unsupported operation: {op}")

