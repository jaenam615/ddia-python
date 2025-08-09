from chapter_3.mini_db.common.utils import pack_record, unpack_record


def test_pack_unpack_roundtrip():
    key = b"alpha"
    val = b"bravo-charlie"
    rec = pack_record(key, val)
    k2, v2 = unpack_record(rec)
    assert k2 == key
    assert v2 == val

