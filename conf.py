# coding=utf8
import os
from pyutil.program.conf_loader import ConfLoader
from pyutil.program.exception import FileNotFound


def string2list(s, sep=','):
    return [i.strip() for i in s.split(sep)]


class Conf(object):

    def __init__(self, filename):
        if not os.path.exists(filename):
            raise FileNotFound
        self.conf_loader = ConfLoader(filename)
        self.conf = self.conf_loader.parse()
        self.local_conf = {}
        try:
            import socket
            self.local_conf['local_ip'] = socket.gethostbyname(
                socket.gethostname())
        except:
            self.local_conf['local_ip'] = ''

    def get_values(self, key):
        val = self.local_conf.get(key) or self.conf.get(key)
        if val:
            return [p.strip() for p in val.split(',')]
        return []

    def get(self, key, val='', check_key_exist=False):
        if check_key_exist:
            if key not in self.local_conf and key not in self.conf:
                raise AttributeError('key: %s not exist' % key)
        value = self.local_conf.get(key) or self.conf.get(key)
        return value or val

    def get_all(self):
        all_kv = self.conf
        all_kv.update(self.local_conf)
        return all_kv

    def set(self, key, value):
        self.conf[key] = value

    def __getattr__(self, name):
        '''
            当 name 不存在时，必须抛出异常
        '''
        try:
            return super(Conf, self).__getattr__(name)
        except:
            return self.get(name, check_key_exist=False)

