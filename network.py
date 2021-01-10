# coding=utf-8
from future.backports.urllib.parse import urlparse


def replace_host(url, host):
    """
    将一个url的host替换成为目标host, 生成新的url.
    :param url:
    :param host:
    :return:
    """
    if url is None:
        return ''
    pr = urlparse(url)
    r = pr._replace(netloc=host)
    return r.geturl()
