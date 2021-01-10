# coding=utf-8
import six
from numpy import unicode
from urllib.parse import urlparse



CDN_HTTPS_HOST = 'https://cdn.x.com/'
# 公共
CDN_HOST = 'https://cdn.picknewsforyou.com/'
# 因为这个帐号是私人帐号, 所以弃用
# CDN_HOST_BIG_NEWS = 'https://cdn.getnewseveryday.com'
CDN_DOMAIN = 'cdn.picknewsforyou.com'

# 缺省来源图标
SOURCE_DEFAULT_ICON = '/icons/article/source_default@3x.png'


def join_cdn_url(path, app_id=''):
    # 低版本 py 上, 如果 path 为 unicode 而非 str, 会抛异常
    if isinstance(path, unicode):
        path = path.encode('utf-8')
    cdn_host = CDN_HOST
    return urlparse.urljoin(cdn_host, path)


def change_cdn_host(url):
    if CDN_HTTPS_HOST in url:
        return urlparse.urljoin(CDN_HOST, url.split(CDN_HTTPS_HOST)[-1])
    return url
