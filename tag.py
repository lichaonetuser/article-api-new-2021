# coding=utf-8
import zlib

TAG_HOT = {'id': 1, 'name': u'人気', 'color': '#f75b5b'}
TAG_IMPORTANT = {'id': 2, 'name': u'トレンド', 'color': '#fc8c1f'}
TAG_DISCUSSED = {'id': 3, 'name': u'話題', 'color': '#8b6de1'}
TAG_LOCATION = {'id': 4, 'name': u'地域', 'color': '#6192f6'}
TAG_LOCATION_DETAIL = {'id': 5, 'name': u'', 'color': '#6192f6'}

TAGS = (TAG_HOT, TAG_IMPORTANT, TAG_DISCUSSED, TAG_LOCATION)

# 数据端和API输出的映射
TAG_DATA_ADAPT_MAP = {
    'is_hot': TAG_HOT,
    'is_important': TAG_IMPORTANT,
    'is_discussed': TAG_DISCUSSED,
}

CITY_TAG_ID_OFFSET = 10000000


def make_tag(name, color):
    # 2, 3 compatible
    id_ = zlib.adler32(name.encode('utf-8'))
    return {'id': id_, 'name': name, 'color': color}


def make_city_tag(name):
    # id_ = zlib.adler32(name.encode('utf-8'))
    # r = {'id': id_, 'name': name, 'color': '#6192f6'}
    # r['name'] = name
    return make_tag(name, '#6192f6')


def make_sport_tag(name):
    return make_tag(name, '#6192f6')
