# coding=utf-8
import time
from pyutil.text.conv import try_parse
from bson import ObjectId


def get_udid_timestamp(udid):
    """
    sample: 15181922390020607v6.5
    :param udid:
    :return: seconds
    """
    if not udid or len(udid) < 17:
        return 0
    elif udid.startswith('mg'):
        ss = udid.split('_')
        if len(ss) > 1:
            x = ObjectId(ss[1])
            return int(time.mktime(x.generation_time.timetuple()))
    else:
        ts = try_parse(udid[:17], int, 0)
        return ts / 10000000
    return 0
