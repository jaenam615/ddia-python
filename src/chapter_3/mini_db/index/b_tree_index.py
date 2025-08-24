from bisect import bisect_left
from typing import List, Tuple

from chapter_3.mini_db.interfaces.index_interface import IndexInterface


class BTreeIndex(IndexInterface):
    """
    교육용 간단 B-Tree 스타일 인덱스 (실제로는 정렬 리스트 + 이진 탐색).
    - 키는 bytes, loc은 tuple로 저장합니다.
    - put/get/delete API는 IndexInterface와 동일합니다.
    - 보너스: range_search(start, end) 제공(옵션)
    """

    def __init__(self):
        self._keys: List[bytes] = []  # 정렬 상태 유지
        self._locs: List[Tuple] = []  # _keys와 동일 인덱스
        self._map: dict[str, Tuple] = {}

    def _find_pos(self, key: bytes) -> int:
        return bisect_left(self._keys, key)

    def put(self, key: bytes, loc: tuple) -> None:
        khex = key.hex()
        if khex in self._map:
            # 기존 위치 업데이트
            pos = self._find_pos(key)
            # 동일 키가 여러번 들어가지 않도록 보장
            if pos < len(self._keys) and self._keys[pos] == key:
                self._locs[pos] = loc
            else:
                # 예외 상황: 맵에는 있는데 키 배열에 없다면 삽입
                self._keys.insert(pos, key)
                self._locs.insert(pos, loc)
        else:
            pos = self._find_pos(key)
            self._keys.insert(pos, key)
            self._locs.insert(pos, loc)
        self._map[khex] = loc

    def get(self, key: bytes) -> tuple | None:
        return self._map.get(key.hex())

    def delete(self, key: bytes) -> None:
        khex = key.hex()
        if khex not in self._map:
            return
        pos = self._find_pos(key)
        if pos < len(self._keys) and self._keys[pos] == key:
            self._keys.pop(pos)
            self._locs.pop(pos)
        self._map.pop(khex, None)

    # 선택적 범위 검색 (인터페이스에는 없지만 제공)
    def range_search(self, start: bytes | None, end: bytes | None) -> List[tuple[bytes, tuple]]:
        start_pos = 0 if start is None else self._find_pos(start)
        results: List[tuple[bytes, tuple]] = []
        for i in range(start_pos, len(self._keys)):
            k = self._keys[i]
            if end is not None and k >= end:
                break
            results.append((k, self._locs[i]))
        return results

