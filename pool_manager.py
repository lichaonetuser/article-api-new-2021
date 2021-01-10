# coding=utf-8
import MySQLdb
import yaml
from DBUtils.PooledDB import PooledDB
from MySQLdb.cursors import DictCursor
from kafka import KafkaProducer, KafkaConsumer

import redis
from future.utils import iteritems, lmap


class BasePoolManager(object):
    @classmethod
    def load_from_yaml(cls, path):
        with open(path, 'r', encoding='UTF-8') as fp:
            config_map = yaml.load(fp, Loader=yaml.FullLoader)
            return cls(config_map)

    def get(self, item):
        return self[item]


class RedisPoolManager(BasePoolManager):
    def __init__(self, config_map):
        """
        :type config_map: dict
        """
        self.config_map = config_map
        self.pools = {}
        for k, v in iteritems(config_map):
            assert k is not None and k.strip() != '' and k not in self.pools
            if isinstance(v, (list, tuple)):
                self.pools[k] = map(lambda x: redis.ConnectionPool(**x), v)
            else:
                self.pools[k] = redis.ConnectionPool(**v)

    def __getitem__(self, pool_name):
        """
        根据 pool name, 获得指定连接的实例
        :type pool_name: str
        :rtype: redis.ConnectionPool|list[redis.ConnectionPool]
        """
        return self.pools[pool_name]  # 如果不存在,抛 KeyError


class MySQLPoolManager(BasePoolManager):
    def __init__(self, config_map, cursor_class=DictCursor):
        self.config_map = config_map
        self.pools = {}
        for k, v in iteritems(config_map):
            assert k is not None and k.strip() != '' and k not in self.pools
            if isinstance(v, (list, tuple)):
                self.pools[k] = lmap(lambda x: PooledDB(MySQLdb, cursorclass=cursor_class, **x), v)
            else:
                self.pools[k] = PooledDB(MySQLdb, cursorclass=cursor_class, **v)

    def __getitem__(self, pool_name):
        """
        :type pool_name: str
        :rtype: DBUtils.PooledDB.PooledDB|list[DBUtils.PooledDB.PooledDB]
        """
        return self.pools[pool_name]


class KafkaProducerPoolManager(BasePoolManager):
    def __init__(self, config_map):
        self.config_map = config_map
        self.pools = {}
        for k, v in iteritems(config_map):
            assert k is not None and k.strip() != '' and k not in self.pools
            if isinstance(v, (list, tuple)):
                self.pools[k] = lmap(lambda x: KafkaProducer(**x), v)
            else:
                self.pools[k] = KafkaProducer(**v)

    def __getitem__(self, item):
        """
        :type item: str
        :rtype: kafka.KafkaProducer
        """
        return self.pools[item]

class MemcachedPoolManager(BasePoolManager):
    def __init__(self, config_map):
        self.config_map = config_map
        self.pools = {}
        for k, v in iteritems(config_map):
            assert k is not None and k.strip() != '' and k not in self.pools

    def __getitem__(self, item):
        return self.pools[item]
