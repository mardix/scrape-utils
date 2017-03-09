
from scrape_utils import BloomFilter

def test_bloom_filter():
    bf = BloomFilter()
    bf.add("hello")
    bf.add("dos")
    bf.add("amigos")
    assert bf.contains("hello")
    assert "dos" in bf
    assert "mocha" not in bf
