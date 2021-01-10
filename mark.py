# coding=utf-8
import logging
import redis
from pyutil.text.conv import is_blank


class MarkDAL(object):
    """
    Guide卡业务规则
    """
    def __init__(self, key_pat, redis_pool, interval=24 * 3600 * 7):
        self.cli = redis.StrictRedis(connection_pool=redis_pool)
        self.interval = interval
        self.key_pat = key_pat

    def need(self, label, pk, interval=None):
        if is_blank(pk):
            return False
        try:
            k = self.key_pat.format(label, pk)
            r = self.cli.get(k)
            if r:
                return False
            if not r:
                interval = self.interval if interval is None else interval
                self.cli.set(k, 1, ex=interval)
                return True
        except:
            logging.getLogger('exc').exception('MarkDAL.need()_error: label={}, pk={}'.format(label, pk))
            return False
