# coding=utf-8
from future.utils import iteritems


def group_by(items, key_fn, extractor=None):
    """
    :type items: list[dict]
    :type key_fn: dict -> Any
    :type extractor: dict -> Any
    :rtype: dict
    """
    ret = {}
    for item in items:
        k = key_fn(item)
        v = item if extractor is None else extractor(item)
        if k in ret:
            ret[k].append(v)
        else:
            ret[k] = [v, ]
    return ret


def reverse_enumerate(coll):
    """
    反向 enumerate()
    eg:
        s = ['a', 'b', 'c', 'd']
        for i, n in reverse_enumerate(s):
            print i, n

        > 3, 'a'
        > 2, 'b'
        > 1, 'c'
        > 0, 'd'
    :param coll:
    :return:
    """
    n = len(coll)
    for i, x in enumerate(coll):
        yield n - i - 1, x


def merge_actions(ops, action_key, value_key, neg_action):
    """
    合并一个操作序列, 每个操作用 dict 来表示

    eg:
        [{action_type: 1, id: 2}, {action_type}:
    :type seq: list[dict]
    :type pos_predicate: (dict) -> bool
    :type neg_predicate: (dict) -> bool
    :type value_key: str
    :type pos_neg_map: dict
    :type neg_pos_map: dict
    :rtype: dict
    """
    # True = add op, False = delete op
    bookings = {}
    for op in ops:
        ac = op[action_key]
        v = op[value_key]
        is_pos = ac != neg_action
        if v in bookings:
            if bookings[v] == is_pos:
                # 如果该值的操作类型和新的一致, 跳过
                continue
            if bookings[v] is True and not is_pos:
                del bookings[v]
            elif bookings[v] is False and is_pos:
                # bookings[v] is False and is_pos 的情况
                # 这表示如果先删,再新加,则等价于新加
                bookings[v] = is_pos
        else:
            bookings[v] = is_pos
    return bookings


def stringify_dict_values(in_dict, out_dict):
    """
    :type in_dict: dict
    :type out_dict: dict
    :rtype: dict
    """
    for k, v in iteritems(in_dict):
        out_dict[k] = repr(v)
    return out_dict


def merge_dict(*dicts, **kwargs):
    ret = {}
    for m in dicts:
        ret.update(m)
    ret.update(kwargs)
    return ret


class AttrDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __getitem__ = dict.__getitem__

    @staticmethod
    def make(*args, **kwargs):
        r = AttrDict()
        for arg in args:
            if isinstance(arg, dict):
                r.update(arg)
            elif hasattr(arg, '__dict__'):
                r.update(arg.__dict__)
        r.update(kwargs)
        return r
