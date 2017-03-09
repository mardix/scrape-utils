"""
BloomFilter

To check the existence of a items

It uses memory and redis

ie:

    bf = BloomFilter()
    bf.add("hello")
    bf.add("jones")

    if "jones" in bf:
        print("It has it")

    if not bf.contains("bossa"):
        print("That's it!")

"""

from bitarray import bitarray
import mmh3

__all__ = ["BloomFilter"]

class BloomFilter(object):

    def __init__(self, size=500000, hash_count=7, connection=None, key="BloomFilter", init_data=None):
        """
        :param size: The size
        :param hash_count: The hash count
        :param connection: A redis connection
        :param key: The redis key name
        :param init_data: Initialize data
        """
        self.size = size
        self.hash_count = hash_count
        self.connection = connection
        self.redis_key = key
        if self.connection:
            pass
        else:
            self.bit_array = bitarray(size)
            self.bit_array.setall(0)

        if init_data:
            self.extends(init_data)

    def add(self, item):
        """
        Add data
        :param item: the item to add
        :return:
        """
        pipeline = self.connection.pipeline() if self.connection else None
        for seed in range(self.hash_count):
            result = mmh3.hash(item, seed) % self.size
            if self.connection:
                pipeline.setbit(self.redis_key, result, 1)
            else:
                self.bit_array[result] = 1
        if self.connection:
            pipeline.execute()

    def contains(self, item):
        if self.connection:
            pipeline = self.connection.pipeline()
            for seed in range(self.hash_count):
                result = mmh3.hash(item, seed) % self.size
                pipeline.getbit(self.redis_key, result)
            return all(pipeline.execute())
        else:
            for seed in range(self.hash_count):
                result = mmh3.hash(item, seed) % self.size
                if self.bit_array[result] == 0:
                    return False
            return True

    def __contains__(self, item):
        return self.contains(item)

    def extends(self, data):
        """
        To add data
        :param data:
        :return:
        """
        return [self.add(d) for d in data]