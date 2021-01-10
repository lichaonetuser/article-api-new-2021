# coding=utf-8
try:
    import simplejson as json
except ImportError:
    import json


def try_parse(v, factory, def_val):
    try:
        return factory(v)
    except:
        return def_val


def is_blank(s):
    return True if s is None or s.strip() == '' else False


def try_load_json(s, def_val=[]):
    return try_parse(s, json.loads, def_val)


def parse_delimiter_list(s, sep=',', factory=int):
    """
    解析分隔序列, 生成列表
    >>> parse_delimiter_list('1,2,3,5', sep=',', factory=int)
    [1, 2, 3, 5]

    :param s:
    :param sep:
    :param factory:
    :return:
    """
    if is_blank(s):
        return []
    r_list = s.split(sep)
    ret = []
    for item in r_list:
        if is_blank(item):
            continue
        ret.append(factory(item))
    return ret
