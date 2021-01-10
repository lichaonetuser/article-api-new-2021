# coding=utf-8
from math import log, pow, e, ceil
import redis
import mmh3


def calc_bloom_filter_params(error_rate, n):
    """
    计算 Bloom Filter 相关配置参数
    :param error_rate: 假阳性概率
    :param n: 容量
    :return: (m存储位数, hash 函数个数(层数)k)
    """
    assert 0 <= error_rate <= 1 and n > 0
    m = ceil((n * log(error_rate)) / log(1.0 / pow(2.0, log(2.0))))
    k = round(log(2.0) * m / n)
    return int(m), int(k)


class RedisBloomFilter(object):
    """
    利用 Redis 存储的 Bloom Filter
    """
    def __init__(self, rp, key, n, error_rate=0.0001, hash_func=mmh3.hash):
        """
        :type rp: redis.ConnectionPool
        :type key: str
        :type n: int
        :type error_rate: float
        :type hash_func: (str) -> int
        """
        assert hash_func is not None
        self.cli = redis.StrictRedis(connection_pool=rp)
        self.key = key
        self.m, self.k = calc_bloom_filter_params(error_rate, n)
        self.n = n
        self.error_rate = error_rate
        self.hash_func = hash_func

    def add(self, item):
        if item is None:
            return
        hs = self.hash(item)
        with self.cli.pipeline() as p:
            for h in hs:
                p.setbit(self.key, h, 1)
            p.execute()

    def contains(self, item):
        if item is None:
            return False
        hs = self.hash(item)
        with self.cli.pipeline() as p:
            for h in hs:
                p.getbit(self.key, h)
            bits = p.execute()
            for bit in bits:
                if bit == 0:
                    return False
        return True

    def hash(self, v):
        """
        求 k 个 hash 值
        :param v:
        :return:
        """
        hs = []
        for i in range(self.k):
            hs.append(self.hash_func(v + str(i)) % self.m)
        return hs

    def __contains__(self, item):
        return self.contains(item)
