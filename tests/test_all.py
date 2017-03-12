
from scrape_utils import BloomFilter, extract_phone_numbers

def test_bloom_filter():
    bf = BloomFilter()
    bf.add("hello")
    bf.add("dos")
    bf.add("amigos")
    assert bf.contains("hello")
    assert "dos" in bf
    assert "mocha" not in bf


test_phone_numbers ="""
555.123.4565
+1-(800)-545-2468
2-(800)-545-2468
3-800-545-2468
555-123-3456
555 222 3342
(234) 234 2442
(243)-234-2342
1234567890
123.456.7890
123.4567
123-4567
1234567900
12345678900
6378743392
(909 703-5086)
I would like for you to give me your phone number now 704)564-9476 704)564-9473 just kidding yo know what I mean 3672 Baxter Cali Bush, Boom Rang CA
100% real fun and friendly no games NO DRAMA no worries with me! kylie - 858-287-7014
1 (234) 567-8901
1.234.567.8901
1/234/567/8901
12345678901
1-234-567-8901 ext. 1234
(+351)282 433 5050
+17048593384
12345678901234567890
1
12
123
1234
12345
123456
1234567
""".strip()
