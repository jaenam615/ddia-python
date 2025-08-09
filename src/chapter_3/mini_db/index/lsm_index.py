from chapter_3.mini_db.interfaces.index_interface import IndexInterface


class LSMIndex(IndexInterface):
    """
    교육용 LSM 인덱스의 단순화 버전:
    - 최신 키는 메모리에 저장("mem" 위치)
    - flush/compaction 시 각 키는 특정 segment("sst", base, offset, length)를 가리키도록 갱신
    - 내부적으로는 해시맵과 유사하지만, 개념상 LSM 계층을 나타내는 명칭을 사용
    """

    def __init__(self):
        self._idx: dict[str, tuple] = {}

    def put(self, key: bytes, loc: tuple) -> None:
        self._idx[key.hex()] = loc

    def get(self, key: bytes) -> tuple | None:
        return self._idx.get(key.hex())

    def delete(self, key: bytes) -> None:
        self._idx.pop(key.hex(), None)

