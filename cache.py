# coding=utf-8
import six
import functools
import abc
if six.PY2:
    import cPickle as pickle
else:
    import pickle


class AbstractSerializer():
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def serialize(self, data):
        pass

    @abc.abstractmethod
    def deserialize(self, data):
        pass


class PickleSerializer(AbstractSerializer):

    def __init__(self):
        super(PickleSerializer, self).__init__()

    def deserialize(self, data):
        return pickle.loads(data)

    def serialize(self, v):
        return pickle.dumps(v)


pickle_ss = PickleSerializer()


class Cache(object):
    """
    Memcached cache decorator class.
    usage:

        c = Cache(memcache.Client(['127.0.0.1']))

        @c.cache('c.calc.{}')
        def x():
            return val

    """
    def __init__(self, mc, serializer=None):
        self.mc = mc
        self.serializer = serializer

    def cache(self, pattern, expires=0, is_bound=False):
        """
        pattern ref:
            https://docs.python.org/2/library/string.html#format-string-syntax

        :param is_bound: 没有办法在运行时拿到方式是否为bound-method
        :param pattern:
        :param expires:
        :return:
        """
        def _0(f):
            @functools.wraps(f)
            def _1(*args, **kwargs):
                # skip the first argument like `self`, `cls`
                key_args = args
                if is_bound:
                    key_args = args[1:]
                key = pattern.format(*key_args, **kwargs)
                val = self.mc.get(key)
                if val is not None:
                    if self.serializer:
                        return self.serializer.deserialize(val)
                    return val
                else:
                    val = f(*args, **kwargs)
                    val_s = val
                    if self.serializer:
                        val_s = self.serializer.serialize(val)
                    self.mc.set(key, val_s, time=expires)
                    return val
            return _1
        return _0

    def set_cache_data(self, pattern, v, expires, *args, **kwargs):
        """
        直接修改缓存数据
        :param pattern:
        :param v:
        :param args:
        :param kwargs:
        :return:
        """
        if v is None:
            return 0
        key = pattern.format(*args, **kwargs)
        if self.serializer:
            v = self.serializer.serialize(v)
        self.mc.set(key, v, time=expires)
        return 1

    def get_cache_data(self, pattern, *args, **kwargs):
        """
        获得缓存过的数据,如果没有被缓存,则返回空.
        使用场景:
            1. 若干数据来源混用同一个cache key.
            2. 人工更新缓存.

        :param pattern:
        :param args:
        :param kwargs:
        :return:
        """
        key = pattern.format(*args, **kwargs)
        val = self.mc.get(key)
        if val is not None:
            if self.serializer:
                return self.serializer.deserialize(val)
            return val
        return None

    def incr(self, pattern, *args, **kwargs):
        """
        原子增缓存中的计数器, 值类型必须为整数
        :param pattern:
        :param args:
        :param kwargs:
        :return:
        """
        key = pattern.format(*args, **kwargs)
        self.mc.incr(key)

    def decr(self, pattern, *args, **kwargs):
        """
        原子减缓存中的计数器,值类型必须为整数
        :param pattern:
        :param args:
        :param kwargs:
        :return:
        """
        key = pattern.format(*args, **kwargs)
        self.mc.decr(key)

    def delete(self, pattern, *args, **kwargs):
        """
        删除缓存key
        :param pattern:
        :param args:
        :param kwargs:
        :return:
        """
        key = pattern.format(*args, **kwargs)
        self.mc.delete(key)

if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(10000)
    import memcache
    mc = memcache.Client(['127.0.0.1:11211'])
    cache = Cache(mc, serializer=pickle_ss)

    @cache.cache('c.f.{}')
    def fib(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return fib(n - 2) + fib(n - 1)

    print(fib(10))

    v = cache.get_cache_data('c.f.{}', 10)
    print('v:', v)

    cache.set_cache_data('c.f.{}', 1000, 0, 10)
    v1 = cache.get_cache_data('c.f.{}', 10)
    print('v1:', v1)
