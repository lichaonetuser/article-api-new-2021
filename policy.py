# coding=utf-8
"""
一些脏逻辑判断都放到这里
"""
from __future__ import absolute_import
import logging

import api.settings
from api.constants import EnumChannelType
from pyutil.api.api_util import QueryStr
from pyutil.text.conv import is_blank
from api.sns_item.models import TwitterImage
from api.utils.api import APIModel
from api.utils.model import ActionMixin
from api.utils.tag import TAG_LOCATION, make_city_tag
from api.utils.version import ver_gte

DISPLAY_TIME_SPAN = 3600 * 3 * 1000
LOCATION_UNKNOWN_KEY = 'unknown'

# 20181015 21:00:00 开始
PURE_MORE_START_TS = 15396084000000000
PURE_TEST_UDIDS = {'xuyuzong', '15363068030020473v7.1.0', '15180960220020628v6.5'}


def fix_image_num_of_line(image, chid, channel_type):
    if not isinstance(image, TwitterImage) or channel_type != EnumChannelType.IMAGE:
        return

    if chid not in {26}:
        image.number_of_lines = 2


def fix_item_display_time(now_ts, item):
    if not item:
        return
    try:
        if (now_ts - item.published_at) < DISPLAY_TIME_SPAN:
            item.display_time = item.published_at
    except:
        logging.getLogger('exc').exception('fix_feed_item_display_time()_err:item={}'.format(item))


REVIEW_BAN_SOURCE_IDS = {
    8913182, 8513771, 3215987, 4738421, 4126406, 4265477, 3517090, 7743516, 8044675, 3720003, 4738527, 9415145, 4265670,
    3242617, 3612107, 3548980, 9414999, 8174001, 4943222, 8913146, 8277492, 8279469, 3548769, 8113349, 8277309, 8805650,
    7682, 9116596, 8915173, 8835737, 1203, 9832947, 10029929, 16689283, 16740547, 16742066, 16742365, 16742616,
    16772686, 17297608, 17930621, 18099597, 18139902, 18141663, 18518474, 18762229, 18761682, 18968766, 18968832,
    18968824, 19741791, 19741765, 19741781, 19743045, 19926243, 19926321, 19926351, 20041626, 20042103, 20284288,
    20284355, 20284371, 20635786, 21393734, 21393747, 23026166, 23434015, 25906192, 25906308, 25906393, 25906473,
    28360941, 28361024, 28361059, 29105909, 29515357, 30271987, 30965538, 30965707, 32874014, 21071325, 1647, 148502,
    1086, 33413, 1479, 8974112, 73047
}


def rule_filter_item_review(item):
    return hasattr(item, 'source_id') and item.source_id in REVIEW_BAN_SOURCE_IDS


def rule_filter_in_alpha_stage(item, query_str):
    """
    版权谈判内测期间使用
    """
    if settings.DEBUG:
        return False
    if query_str.phone_type == 'iphone':
        return False
    if isinstance(item, APIModel):
        return hasattr(item, 'copyright_source_id') and item.copyright_source_id == 87
    elif isinstance(item, dict):
        return item.get('copyright_source_id', 0) == 87
    else:
        return False


def fix_item_display_options(item, version, channel_style):
    """
    计算 display_options 字段
    """
    if not hasattr(item, 'display_options'):
        return
    if hasattr(item, 'display_time') and item.display_time > 0:
        item.display_options = 0b1
    elif hasattr(item, 'comment_count') and item.comment_count > 0:
        item.display_options = 0b10

    # kijiji的文章, 控制开关, 去掉source图标显示
    if rule_is_kijiji(item):
        item.display_options |= 0b100


def fix_item_tags(item, city_code, is_local=False):
    # 处理从数据过来的 tag 信息
    if isinstance(item, ActionMixin):
        item.adapt_tags()
    return
    # XXX  由于地域不准, 20181017 下掉了地域标签
    if item.location:
        if is_local:
            # 如果是本地频道进来, 就说明prefecture本身已经是item.city_code[:2]了
            town_city_prefecture = (
                item.location.get('town_name', LOCATION_UNKNOWN_KEY),
                item.location.get('city_name', LOCATION_UNKNOWN_KEY),
            )
            r = LOCATION_UNKNOWN_KEY
            for k in town_city_prefecture:
                if k == LOCATION_UNKNOWN_KEY:
                    continue
                r = k
                break
            if r != LOCATION_UNKNOWN_KEY:
                item.tags.append(make_city_tag(r))

        elif len(city_code) >= 2:
            item_city_code = item.location.get('city_code', '')
            if len(item_city_code) < 2:
                return
            code_pre = item_city_code[:2]
            if code_pre == city_code[:2]:
                item.tags.append(TAG_LOCATION)


def fix_twitter_image_card(item, chid, query_str):
    """
    漫画频道使用twitter card的方式
    :return:
    """
    if query_str.unique_device_id in {'15206849840020612v6.5.2', }:
        # 兼容客户端bug
        return item
    if ver_gte(query_str.version, '6.8.1') and chid == 25 and isinstance(item, TwitterImage):
        return item.as_twitter_card()
    return item


def rule_is_kijiji(item):
    return hasattr(item, 'copyright_source_id') and item.copyright_source_id == 1


def rule_is_pure(query_str):
    """
    受苹果商店推荐影响的用户
    """
    return False
    if query_str.unique_device_id in PURE_TEST_UDIDS:
        return True
    udid = query_str.unique_device_id
    if query_str.phone_type == QueryStr.PHONE_TYPE_ANDROID or is_blank(udid) or udid.startswith('mg'):
        return False
    if len(udid) < 23:
        return False
    try:
        ts = int(udid[:17])
        if ts > PURE_MORE_START_TS:
            return True
    finally:
        return False


KIJI_WHITE_SOURCE_IDS = {
    7682, 1002992, 3215987, 3242617, 3517090, 3548769, 3548980, 3612107, 3720003, 4126406, 4265477, 4265670, 4738421,
    4738527, 4943222, 7743516, 8044675, 8113349, 8174001, 8277309, 8277492, 8279469, 8513771, 8516223, 8835737,
    8913146, 8913182, 8915173, 9414999, 9415145, 9832947, 16689283, 16690150, 16716681, 16740284, 16740547, 16742066,
    16742219, 16742365, 16742616, 16772686, 17248538, 17297608, 17298375, 17302145, 17303970, 17930621, 17931361,
    17953516, 17953625, 17953727, 18099597, 18138524, 18139229, 18139902, 18141663, 18518474, 18529573, 18531403,
    18531484, 18531661, 18761682, 18762062, 18762229, 18762251, 18762261, 18968766, 18968820, 18968824, 18968832,
    19153321, 19741760, 19741765, 19741768, 19741781, 19741791, 19743045, 19926243, 19926321, 19926332, 19926336,
    19926346, 19926351, 20041626, 20041793, 20041870, 20041958, 20042103, 20275720, 20275845, 20284271, 20284288,
    20284355, 20284371, 20284376, 20635786, 20635813, 20635840, 20635846, 21393633, 21393680, 21393713, 21393734,
    21393747, 21393779, 23025712, 23025868, 23025955, 23026058, 23026166, 23434015, 23434046, 23769962, 23774665,
    25906192, 25906244, 25906308, 25906393, 25906473, 28360941, 28360979, 28361024, 28361059, 28585220, 29105848,
    29105873, 29105909, 29105932, 29105963, 29515075, 29515260, 29515357, 30271987, 30272773, 30273754, 30274524,
    30275142, 30275790, 30965487, 30965538, 30965625, 30965671, 30965707, 32873951, 32874014, 32874067, 32874102,
    32874126, 34720586, 34720713, 34720776, 34720844, 35147192, 35147899, 35778540, 35778598, 35778630, 35778680,
    35778700, 36981299, 36981335, 36981380, 36981395, 36981430, 37482724, 37482757, 37482776, 37482805, 38421955,
    38421976, 38422011, 38422030, 38422054, 39682084, 39682108, 39682131, 39682166, 39682217, 43649525, 43649575,
    43649611, 43649643, 56629919, 56630300, 56630393, 56630407, 56630418, 56630601, 56635512, 56635546, 56635553,
    56635679, 56635707, 56635714, 56635732, 56635745, 56635754, 56635760, 56635795, 56635802
}


def rule_filter_kiji_white_source(item):
    return item.source_id in KIJI_WHITE_SOURCE_IDS


def rule_is_nor_source(item):
    return item.copyright_source_id == 1
