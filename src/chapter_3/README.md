database
├── interfaces
│   ├── storage_engine_interface.py   # read/write API 정의
│   ├── index_interface.py            # 인덱스 검색 API 정의
│   └── transaction_manager_interface.py # 트랜잭션 관리 API
│
├── common
│   ├── utils.py
│   ├── errors.py
│   └── config.py
│
├── storage
│   ├── memtable.py
│   ├── ss_table.py
│   └── wal.py   # write-ahead log
│
├── index
│   ├── hash_index.py
│   ├── b_tree_index.py
│   └── lsm_index.py
│
├── processing
│   ├── oltp.py
│   └── olap.py   # 나중에 구현
│
└── manager
    ├── transaction_manager.py
    ├── query_executor.py
    └── catalog_manager.py