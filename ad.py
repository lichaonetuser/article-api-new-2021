# coding=utf-8
"""
简单列表广告逻辑
"""
from __future__ import absolute_import
import copy
import hashlib
import random
import uuid

from datetime import datetime
import time

from pyutil.text.conv import try_parse
from pyutil.constants import AppIds
from pyutil.api.traffic import select_by_udid
from pyutil.program.db_ctx import DbExec
from api.utils.api import APIModel, is_review_mode
from api.utils.model import FeedItemMixin

from api.constants import EnumChannelType
from api.constants import EnumItemType
from api.settings import mysql_pool
from api.utils.qs import get_udid_timestamp
from api.utils.time_util import current_timestamp
from api.utils.version import ver_lt, ver_gte

from api.log import exception_logger, api_logger

AD_INSERT_POS = 3
DOKI_INSERT_POS = 4

# doki卡片放出时间配置
DOKI_LAUNCH_TIME = {
    0: (17, 23),
    1: (17, 23),
    2: (17, 23),
    3: (17, 23),
    4: (17, 23),
    5: (11, 23),
    6: (11, 23),
}

local_doki_cache = {'time': 0}

def get_doki_time():
    if time.time() < local_doki_cache['time'] and local_doki_cache.get('value'):
        return local_doki_cache['value']
    doki_launch_time = copy.deepcopy(DOKI_LAUNCH_TIME)
    try:
        ex = DbExec(mysql_pool['static_data'])
        ex.query('set names utf8mb4;')
        rows = ex.query('select week_day, start_hour, end_hour from ad_launch where ad_name=%s and week_day<7', ('feed_ad_doki', ))
        for rc in rows:
            doki_launch_time[rc['week_day']] = (rc['start_hour'], rc['end_hour'])
    except Exception as e:
        exception_logger.exception('get except:{}'.format(e))
    local_doki_cache['value'] = doki_launch_time
    local_doki_cache['time'] = time.time() + 1200
    api_logger.info('local_doki_cache:{}'.format(local_doki_cache))
    return doki_launch_time


def gen_check_id(source_id):
    m0 = hashlib.md5()
    m0.update('{}zwb6uAr^J'.format(source_id))
    m0s = m0.hexdigest().upper()
    m1 = hashlib.md5()
    m1.update(m0s)
    return m1.hexdigest().upper()


class AdSource(object):
    ADMOB = 'admob'
    MOPUB = 'mopub'
    XYZ = 'xyz'
    FACEBOOK = 'facebook'
    JUMPRAW = 'jumpRaw'


class AdType(object):
    FEED_RIGHT_IMAGE = 10
    FEED_LARGE_IMAGE = 11
    FEED_VIDEO = 12

    SOURCE_ID_MAP = {
        "iphone": {
            AdSource.ADMOB: {
                FEED_RIGHT_IMAGE: 'ca-app-pub-9086589736901942/2938802883',
                FEED_LARGE_IMAGE: 'ca-app-pub-9086589736901942/3181457413',
                FEED_VIDEO: 'ca-app-pub-9086589736901942/8191129569'
            },
            AdSource.MOPUB: {
                FEED_RIGHT_IMAGE: 'a43a1752c93c4d10a3542c61390b4303',
                FEED_LARGE_IMAGE: '04eae6fa849a44eb9367bf7d278e5427',
                FEED_VIDEO: 'f668b72f64dd4f4083c5445b3afe2fcf'
            },
            AdSource.XYZ: {
                FEED_RIGHT_IMAGE: "ca-app-pub-2599375973832321/4569163185",
                FEED_LARGE_IMAGE: "ca-app-pub-2599375973832321/6668712917",
                FEED_VIDEO: "ca-app-pub-2599375973832321/9558121207",
            },
            AdSource.FACEBOOK: {
                FEED_RIGHT_IMAGE: "150393252372217_470285010383038",
                FEED_LARGE_IMAGE: "150393252372217_470284750383064",
                FEED_VIDEO: "150393252372217_470284513716421",
            },
            AdSource.JUMPRAW: {
                FEED_RIGHT_IMAGE: "945154001",
                FEED_LARGE_IMAGE: "945087334",
                FEED_VIDEO: "945153998",
            }
        },
        "android": {
            AdSource.ADMOB: {
                FEED_RIGHT_IMAGE: 'ca-app-pub-9086589736901942/7594913288',
                FEED_LARGE_IMAGE: 'ca-app-pub-9086589736901942/4038811655',
                FEED_VIDEO:       'ca-app-pub-9086589736901942/5268186740'
            },
            AdSource.FACEBOOK: {
                FEED_RIGHT_IMAGE: '2344228655832645_2349986005256910',
                FEED_LARGE_IMAGE: '2344228655832645_2349985481923629',
                FEED_VIDEO:       '2344228655832645_2349985878590256'
            },
            AdSource.JUMPRAW: {
                FEED_RIGHT_IMAGE: '10147',
                FEED_LARGE_IMAGE: '10145',
                FEED_VIDEO:       '10146'
            }
        }
    }

    @staticmethod
    def source_id(phone_type, ad_source, ad_type):
        return AdType.SOURCE_ID_MAP.get(phone_type, {}).get(ad_source, {}).get(ad_type, '')

class AD(APIModel, FeedItemMixin):
    def __init__(self, query_str, data=None):
        APIModel.__init__(self)
        FeedItemMixin.__init__(self)
        self.type = EnumItemType.AD
        self.ad_source = AdSource.FACEBOOK
        self.ad_type = AdType.FEED_RIGHT_IMAGE
        self.phone_type = 'iphone'
        self.app_id = ''
        self.source_id = ''
        self.check_id = ''
        self.aid = ''
        self.udid = query_str.unique_device_id
        self.version = query_str.version
        self.init(data)

        if self.app_id not in [AppIds.Article_NewsTime, AppIds.Article_BigNews, AppIds.Article_Android_NewsBox]:
            return

        if self.phone_type == 'android' and self.app_id != "com.box.app.news":
            return

        if self.phone_type == 'iphone':
            xyz_id = AdType.source_id(self.phone_type, AdSource.XYZ, self.ad_type)
            self.xyz = {
                "id": xyz_id,
                "check_id": gen_check_id(xyz_id)
            }
        if (self.phone_type == 'android' and ver_gte(self.version, '7.4.12')) or (self.phone_type == 'iphone' and select_by_udid(self.udid, 2, 10)):
            self.ad_source = AdSource.JUMPRAW

        if (self.phone_type == 'iphone' and ver_gte(self.version, '7.7.10')):
            setattr(self, 'ad_max_loading_duration', 5)
            setattr(self, 'ad_configs', [])
            for source in [AdSource.FACEBOOK, AdSource.JUMPRAW]:
                item = {
                    'ad_source': source,
                    'source_id': AdType.source_id(self.phone_type, source, self.ad_type),
                }
                item['check_id'] = gen_check_id(item['source_id'])
                self.ad_configs.append(item)

        self.source_id = AdType.source_id(self.phone_type, self.ad_source, self.ad_type)
        self.check_id = gen_check_id(self.source_id)

    def as_dict(self):
        INNER_FIELDS = ('app_id', 'version', 'udid')
        return {k: v for k, v in self.__dict__.items() if k not in INNER_FIELDS}

class DokiCard(APIModel, FeedItemMixin):
    def __init__(self, data=None):
        APIModel.__init__(self)
        FeedItemMixin.__init__(self)
        self.type = EnumItemType.DOKI_CARD
        self.aid = ''
        self.init(data)


    def as_dict(self):
        return self.__dict__

def doki_launch(items, query_str, channel_type, tc=0, lc=0):
    """
    :param channel_type: 频道类型
    :param items: 待输出项
    :param query_str: 通参
    :param tc:  total counter
    :param lc:
    :return:
    """
    try:
        if not items:
            return items
        dt_now = datetime.now()
        weekday = dt_now.weekday()
        hour = dt_now.hour
        doki_time = get_doki_time()
        if hour < doki_time[weekday][0] or hour > doki_time[weekday][1]:
            return items

        if channel_type != EnumChannelType.ARTICLE:
            return items

        if is_review_mode(query_str) \
                or (query_str.phone_type == 'iphone' and ver_lt(query_str.version, '7.7.1')) \
                or (query_str.phone_type == 'android' and ver_lt(query_str.version, '7.4.2')):
            return items

        card = DokiCard({'aid': uuid.uuid4().hex, 'phone_type': query_str.phone_type, 'app_id': query_str.app_id})

        if len(items) <= DOKI_INSERT_POS:
            items.append(card)
        else:
            items.insert(DOKI_INSERT_POS, card)
    except:
        exception_logger.exception('ad_launch: {} {} {} {}'.format(items, query_str, channel_type, tc))
    return items

def ad_launch(items, query_str, channel_type, tc=0, lc=0):
    """
    :param channel_type: 频道类型
    :param items: 待输出项
    :param query_str: 通参
    :param tc:  total counter
    :param lc:
    :return:
    """
    try:
        if not items:
            return items

        if channel_type != EnumChannelType.ARTICLE:
            return items

        ts = get_udid_timestamp(query_str.unique_device_id)
        current_ts = int(time.time())
        # 小于3天的广告不出
        if abs(current_ts - ts) < 259200:
            return items

        if is_review_mode(query_str) \
                or (query_str.phone_type == 'iphone' and ver_lt(query_str.version, '7.6.4')) \
                or (query_str.phone_type == 'android' and ver_lt(query_str.version, '7.2.1')):
            return items

        i = tc % 4
        if i == 0:
            ad_type = random.choice((AdType.FEED_LARGE_IMAGE, AdType.FEED_VIDEO))
        elif i == 2:
            ad_type = AdType.FEED_RIGHT_IMAGE
        else:
            return items

        # ad_type = (AdType.FEED_LARGE_IMAGE, AdType.FEED_VIDEO, AdType.FEED_RIGHT_IMAGE)[tc % 3]
        ad = AD(query_str, {
                'ad_type': ad_type,
                'aid': uuid.uuid4().hex, 'phone_type': query_str.phone_type,
                'app_id': query_str.app_id,
             })

        if ad.source_id is None or ad.source_id.strip() == '':
            return items

        if len(items) <= AD_INSERT_POS:
            items.append(ad)
        else:
            items.insert(AD_INSERT_POS, ad)
    except:
        exception_logger.exception('ad_launch: {} {} {} {}'.format(items, query_str, channel_type, tc))
    return items
