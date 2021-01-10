# coding=utf-8
import logging

class LRUSetCache(object):
    """
    基于set顺序的简单内存LRUCache
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.slots = {}
        self.set_list = []
        self.count = 0

    def get(self, key, defval=None):
        v = self.slots.get(key, defval)
        return v

    def put(self, key, value):
        while len(self.set_list) > self.capacity:
            self.slots.pop(self.set_list.pop(0), None)
        self.set_list.append(key)
        self.slots[key] = value
        self.count += 1
        if self.count % 1100 == 0:
            logging.getLogger('api').info('lru put {}:{}, size:{}'.format(key, value, self.count))

    def contains(self, key):
        return key in self.slots
