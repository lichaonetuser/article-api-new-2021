# coding=utf-8
import random
import six
from datetime import datetime

import yaml
from mongoengine import Document, StringField, IntField, DateTimeField


_OCT_DIGIT_TABLE = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 5, '5': 6, '6': 7, '7': 8}
_OCT_OFFSET = 1 if six.PY2 else 2
_MAGIC_START = 189409


class DevicePseudonym(Document):
    """
    设备,假名映射
    """
    meta = {
        'db_alias': 'social',
        'indexes': ['unique_device_id']
    }
    unique_device_id = StringField()
    pseudonym = StringField()
    mtime = DateTimeField(default=datetime.now)


class IdGen(Document):
    """
    使用MongoDB存储ID分配器
    """
    meta = {
        'db_alias': 'social',
        'indexes': ['key']
    }
    key = StringField()
    seq = IntField(default=0)
    mtime = DateTimeField(default=datetime.now)

    @staticmethod
    def get_next_id(key):
        assert key and key.strip() != ''
        r = IdGen.objects(key=key).modify(upsert=True, new=True, key=key, inc__seq=1, mtime=datetime.now())
        return r.seq


class PseudonymGen(object):
    """
    假名生成工具
    """
    def __init__(self, adj_word_list, noun_word_list):
        assert len(adj_word_list) > 0
        assert len(noun_word_list) > 0
        self.adj_word_list = adj_word_list
        self.noun_word_list = noun_word_list

    def _make(self, next_id):
        adj = random.choice(self.adj_word_list)
        noun = random.choice(self.noun_word_list)
        oct_str = oct(next_id)[_OCT_OFFSET:]
        r = 0
        for c in oct_str:
            r = r * 10 + _OCT_DIGIT_TABLE[c]
        return u'{}{}{}'.format(adj, noun, r)

    def gen(self):
        """
        Mongoengine 必须要 connected 的
        """
        next_id = IdGen.get_next_id('pseudonym') + _MAGIC_START
        return self._make(next_id)

    def gen_for(self, unique_device_id):
        if not unique_device_id or unique_device_id.strip() == '':
            raise ValueError('empty unique_device_id')
        r = DevicePseudonym.objects(unique_device_id=unique_device_id).first()
        if r:
            return r.pseudonym
        dp = DevicePseudonym()
        dp.unique_device_id = unique_device_id
        dp.pseudonym = self.gen()
        dp.save()
        return dp.pseudonym

    @staticmethod
    def load_from_yaml(path):
        with open(path, 'r', encoding='UTF-8') as fp:
            m = yaml.load(fp.read(), Loader=yaml.FullLoader)
            return PseudonymGen(m['adj_word_list'], m['noun_word_list'])
