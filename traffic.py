# coding=utf-8
"""
小流量抽取:
    - 按hash()
    - 按概率
"""
import time
import random

from pyutil.text.conv import try_parse


def select_by_prob(ratio=0.1):
    prob = random.random()
    return True if prob <= ratio else False


def select_by_hash(bytes_, ratio_base=10):
    hash_v = hash(bytes_)
    return True if hash_v % ratio_base == 1 else False


def select_by_hash_ex(bytes_, ratio_base=10, expires_base=600):
    """
    select by hash value with expires
    """
    assert expires_base > 0
    time_key = int(time.time() / expires_base)
    return True if (time_key + hash(bytes_)) % ratio_base == 0 else False


def select_by_ret_hash_ex(bytes_, ratio_base=10, expires_base=600):
    """
    select by hash value with expires
    return hash value
    """
    assert expires_base > 0
    time_key = int(time.time() / expires_base)
    return (time_key + hash(bytes_)) % ratio_base


# bit 表示取末尾几位
def select_by_udid(unique_device_id, bit, ratio_min=0):
    if not unique_device_id or unique_device_id.strip() == '':
        return False
    ss = unique_device_id.split('v')
    if not ss:
        return False
    remainder = try_parse(unique_device_id.split('v')[0][-bit:], int, 0)
    return True if remainder < ratio_min else False

def select_by_udid_gte_time(udid, seconds):
    """
    udid 生成时间超过seconds, 返回True
    :param udid:
    :return: bool
    """
    if not udid or len(udid) < 17:
        return False
    try:
        if udid.find('mgd') == 0:
            # android udid format(mongodb id) parse, sample: mgd14_5c823b4ee5640901a5f952de
            ts = int(udid[6:14], 16)
        else:
            # iphone udid format parse, sample: 15135695090020466v6.3
            ts = try_parse(udid[:10], int, 0)
        return time.time() - ts > seconds
    except Exception as e:
        pass
    return False


def get_code_by_hash(bytes_, base=100):
    hash_v = hash(bytes_)
    return hash_v % base

# bit 表示取末尾几位
def select_by_udid_group(unique_device_id, bit, divide=()):
    if not unique_device_id or unique_device_id.strip() == '':
        return 0
    ss = unique_device_id.split('v')
    if not ss:
        return 0
    remainder = try_parse(unique_device_id.split('v')[0][-bit:], int, 0)
    for i, c in enumerate(divide):
        if remainder < c:
            return i+1
    return len(divide) + 1
