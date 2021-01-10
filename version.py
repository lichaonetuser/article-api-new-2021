# coding=utf-8
from distutils.version import StrictVersion


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
