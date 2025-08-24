from chapter_3.mini_db.common.bloom_filter import BloomFilter


def test_bloom_basic_membership(tmp_path):
    keys = [b"a", b"b", b"c"]
    bf = BloomFilter.from_keys(keys, false_positive_rate=0.01)
    for k in keys:
        assert bf.might_contain(k)
    assert not bf.might_contain(b"zzz")

    p = tmp_path / "f.json"
    bf.save_json(str(p))
    bf2 = BloomFilter.load_json(str(p))
    for k in keys:
        assert bf2.might_contain(k)

