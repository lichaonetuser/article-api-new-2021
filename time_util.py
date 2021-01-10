# coding=utf-8
import time
from datetime import date, datetime


def current_timestamp():
    return int(time.time() * 1000)


def today_timestamp():
    return int(time.mktime(date.today().timetuple()) * 1000)


def try_parse_datetime_ts(datetime_str, fmt='%Y-%m-%d %H:%M:%S', def_val=0):
    try:
        dt = datetime.strptime(datetime_str, fmt)
        return int(time.mktime(dt.timetuple()) * 1000)
    except:
        return def_val


def to_timestamp(dt, defval=0):
    """
    :type dt: datetime.datetime
    :type defval: 0
    :rtype: int
    """
    if not dt:
        return defval
    return int(time.mktime(dt.timetuple()) * 1000)
