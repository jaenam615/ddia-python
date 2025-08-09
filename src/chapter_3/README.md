### Chapter 3 — 저장소와 검색: MiniDB (LSM 기반)

이 폴더는 DDIA 3장(저장소와 검색) 내용을 바탕으로 아주 작은 LSM 스타일의 키-값 저장소를 파이썬으로 구현한 예제입니다. 핵심 아이디어는 다음과 같습니다.

- 쓰기 경로: WAL에 기록 → MemTable(In-Memory)에 반영 → 임계치 도달 시 SSTable(불변 Segment)로 flush
- 읽기 경로: 인덱스로 위치 확인 → MemTable 또는 SSTable에서 조회 → Bloom Filter로 음수 조회 가속
- 복구(Recovery): 재시작 시 WAL을 스캔해 MemTable과 인메모리 인덱스를 재구성
- 컴팩션(Compaction): 여러 SSTable을 병합하여 최신값만 남기고 오래된 중복을 제거

### 폴더 구조

```
chapter_3/
  mini_db/
    common/
      bloom_filter.py     # 간단한 Bloom Filter 구현(JSON 직렬화 지원)
      utils.py            # 레코드 프레이밍(pack/unpack) 유틸
      disk_manager.py     # 페이지 단위 파일 관리(데모용)
    engine/
      mini_db.py          # MiniDB 오케스트레이션: set/get/flush/compact
    index/
      hash_index.py       # 키 → 위치(mem 또는 sst)를 가리키는 단순 해시 인덱스
      lsm_index.py
      b_tree_index.py
    interfaces/
      index_interface.py
      storage_engine_interface.py
      disk_manager_interface.py
    processing/
      oltp.py
    storage/
      memtable.py         # 인메모리 Map
      wal.py              # Write-Ahead Log(내구성)
      ss_table.py         # SSTable 세그먼트(.data/.idx/.bloom)
    main.py               # 간단한 데모 실행 스크립트
```

### 내부 동작(Internals)

- WAL(`wal.py`)
  - 각 쓰기는 `[klen(2B)][vlen(4B)][key][value]` 형식의 레코드를 길이 프리픽스(4B)와 함께 파일에 append 합니다.
  - `iter_records()`로 전체 스캔하여 복구 시 MemTable을 재구성합니다.

- MemTable(`memtable.py`)
  - 단순 `dict[bytes, bytes]` 형태의 인메모리 테이블입니다.
  - 임계치(엔트리 수) 이상이 되면 flush 대상이 됩니다.

- SSTable(`ss_table.py`)
  - flush 시 키 정렬 후 `segment_N.data`(레코드 연속 저장)와 `segment_N.idx`(JSON: key_hex → [offset, length]) 생성합니다.
  - `segment_N.bloom`(JSON 직렬화된 Bloom Filter)을 함께 생성하여 존재하지 않는 키 조회를 빠르게 거릅니다.
  - 조회 시 Bloom Filter → 인덱스 확인 → 데이터 파일에서 오프셋으로 점프하여 값 복원.

- 인덱스(`hash_index.py`)
  - 인메모리 해시 맵으로, 값의 위치를 `("mem" | "sst", base, offset, length)` 형태로 저장합니다.
  - 최신 쓰기는 먼저 `("mem", ...)`으로 표시되고, flush/compaction 후 `("sst", ...)`로 업데이트됩니다.

- MiniDB 엔진(`engine/mini_db.py`)
  - `db_set(key: str, value: bytes)`
    1) WAL에 append → 2) MemTable에 put → 3) 인덱스에 `mem` 위치 기록 → 4) 임계치 초과 시 `flush()`
  - `db_get(key: str)`
    - 인덱스 위치를 보고 `mem`이면 MemTable에서, `sst`이면 Bloom Filter/인덱스를 거쳐 Segment에서 값을 읽습니다.
    - 실패 시 최신→오래된 순서로 모든 Segment를 fallback 검색합니다.
  - `flush()`
    - MemTable을 새로운 Segment로 내리고, 인덱스를 해당 Segment로 갱신한 뒤 MemTable을 비우고 WAL을 초기화합니다.
  - `compact()`
    - 여러 Segment를 최신→오래된 순으로 스캔하여 “처음 본(=최신) 값”만 모아 새 Segment를 만들고, 인덱스를 갱신합니다.
    - 데모 단순화를 위해 기존 Segment 파일들은 제거합니다.

### 파일 포맷 요약

- 레코드 프레이밍: `[klen:2][vlen:4][key][value]`
- 데이터 파일: `segment_N.data` (프레이밍된 레코드의 연속)
- 인덱스 파일: `segment_N.idx` (JSON, `key_hex -> [offset, length]`)
- 블룸 파일: `segment_N.bloom` (JSON, `m, k, bits(hex)`)

### 제약사항/향후 작업

- 삭제(Tombstone) 미구현: 삭제 전파와 컴팩션에서의 정리가 없으므로 실제 삭제 기능은 제공하지 않습니다.
- 범위 스캔/정렬 읽기 미구현: 키 정렬로 기록하지만 범위 질의 API는 아직 제공하지 않습니다.
- 동시성/락/트랜잭션 미구현: 단일 스레드/단일 프로세스 사용을 가정합니다.
- 내구성 정책 단순화: 각 쓰기마다 `fsync` 호출(학습용), 배치/그룹 커밋 등은 미구현.

### 실행 방법

```bash
cd /Users/jaeheenam/Dev/personal/ddia-python
PYTHONPATH=src uv run -q python -m chapter_3.mini_db.main
```

### 테스트 실행

```bash
cd /Users/jaeheenam/Dev/personal/ddia-python
PYTHONPATH=src uv run -q pytest -q tests/chapter_3/test_mini_db.py
```

### 간단 사용 예시

```python
from chapter_3.mini_db.engine.mini_db import MiniDB

db = MiniDB(data_dir="/tmp/mini_db_demo", mem_threshold=2)
db.db_set("apple", b"사과")
db.db_set("banana", b"바나나")
print(db.db_get("apple"))  # b"사과"
db.flush()
db.compact()
db.close()
```

### 시퀀스 다이어그램 (ASCII)

아래는 쓰기/읽기/컴팩션의 단순 흐름을 ASCII 다이어그램으로 표현한 것입니다.

1) 쓰기 경로: db_set

```
Client                MiniDB                 WAL            MemTable              Index              SSTableManager             Files
  | db_set(k,v)         |                     |               |                    |                        |                       |
  |-------------------->|                     |               |                    |                        |                       |
  |                     | append(k,v)         |               |                    |                        |                       |
  |                     |-------------------->|               |                    |                        |                       |
  |                     | put(k,v)                            |                    |                        |                       |
  |                     |------------------------------->|     |                    |                        |                       |
  |                     | put(k, ("mem",...))                                  |                        |                       |
  |                     |----------------------------------------------------->|                        |                       |
  |                     | if len(mem) >= threshold?                           |                        |                       |
  |                     |-------------------------------------------- alt ----+------------------------+-----------------------+
  |                     | flush_memtable(items)                                                       |                       |
  |                     |--------------------------------------------------------------------------->|                       |
  |                     |                                                                             | write segment_N.data  |
  |                     |                                                                             | write segment_N.idx   |
  |                     |                                                                             | write segment_N.bloom |
  |                     |                                                                             |<----------------------|
  |                     | update index: ("sst", base, offset, length)                                |                       |
  |                     |-----------------------------------------------------> Index                  |                       |
  |                     | clear mem; wipe WAL                                                           |                       |
  |                     |---------------------------------------> MemTable / WAL                        |                       |
```

2) 읽기 경로: db_get

```
Client                MiniDB                        Index                    MemTable               SSTableManager
  | db_get(k)           |                            |                         |                        |
  |-------------------->|                            |                         |                        |
  |                     | get(k) -> loc              |                         |                        |
  |                     |--------------------------->|                         |                        |
  |                     | if loc == ("mem", ...)                           get(k) -> v                |
  |                     |----------------------------------------------->|        return v            |
  |                     | if loc == ("sst", base, off, len)                                          |
  |                     |                                                    lookup_in_segment(base,k)|
  |                     |---------------------------------------------------------------------------->|
  |                     |    if miss: lookup across segments (Bloom 체크 후 인덱스/파일 접근)        |
  |                     |---------------------------------------------------------------------------->|
  |                     | return v                                                                 |
```

3) 컴팩션: compact

```
Client                MiniDB                         SSTableManager                       Index                   Files
  | compact()           |                             |                                     |                       |
  |-------------------->|  read newest->oldest .idx   |                                     |                       |
  |                     |---------------------------->|                                     |                       |
  |                     |  first-seen wins(최신값만)  |                                     |                       |
  |                     |  flush new compacted segment|------------------------------------>| write compacted files |
  |                     | update index to new_base                                            |                       |
  |                     |--------------------------------------------------------------->|                           |
  |                     | delete old segments (데모용)                                                                |
  |                     |------------------------------------------------------------------------------------------->|
```