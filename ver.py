# coding=utf-8
from distutils.version import StrictVersion


def v_cmp(v0, v1):
    """
    版本号比较函数
    :type v0: str
    :type v1: str
    :rtype: int
    """
    _v0 = StrictVersion(v0)
    _v1 = StrictVersion(v1)
    if _v0 == _v1:
        return 0
    return 1 if _v0 > _v1 else -1


def _ver_cmp(lhs, rhs, f, fail_value=False):
    try:
        lhs_v = StrictVersion(lhs)
        rhs_v = StrictVersion(rhs)
        return f(lhs_v, rhs_v)
    except:
        return fail_value


def ver_lt(lhs, rhs, fail_value=False):
    return _ver_cmp(lhs, rhs, lambda x, y: x < y)


def ver_lte(lhs, rhs, fail_value=False):
    return _ver_cmp(lhs, rhs, lambda x, y: x <= y)


def ver_gt(lhs, rhs, fail_value=False):
    return _ver_cmp(lhs, rhs, lambda x, y: x > y)


def ver_gte(lhs, rhs, fail_value=False):
    return _ver_cmp(lhs, rhs, lambda x, y: x >= y)


def ver_eq(lhs, rhs, fail_value=False):
    return _ver_cmp(lhs, rhs, lambda x, y: x == y)
