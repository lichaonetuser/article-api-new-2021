# coding=utf-8
"""
MemcachedClient Load/Traffic Balance
"""
import memcache
import random
import logging


class _WrapForDrill(object):
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        try:
            return self.fn(*args, **kwargs)
        except Exception as e:
            logging.error("_WrapForDrill:fn={},args={},kwargs={}".format(self.fn, args, kwargs))
            return None


class LBMemcachedClient(object):

    def __init__(self, servers, *args, **kwargs):
        if not servers or not isinstance(servers, (list, tuple)):
            raise TypeError("servers are empty, or not type of (list,tuple)")
        self.clients = []
        for s in servers:
            self.clients.append(memcache.Client((s,), *args, **kwargs))

    def disconnect_all(self):
        for c in self.clients:
            try:
                c.disconnect_all()
            except Exception as e:
                logging.error('Error while disconnect_all.c={},e={}'.format(c, e))

    def _get_client(self):
        return random.choice(self.clients)

    def __getattr__(self, item):
        obj = getattr(self._get_client(), item)
        if obj is None:
            return obj
        if callable(obj):
            return _WrapForDrill(obj)
        return obj
