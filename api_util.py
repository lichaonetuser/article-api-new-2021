#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
from urllib.parse import urlparse

import rncryptor
import time
import redis
from hashlib import md5
from iso3166 import countries
from pyutil.api.types import BaseTypes
from pyutil.api.language import translate_lang_from_request
from pyutil.text.conv import is_blank

intra_company_devices = [ ]

TOKYO_CITIES = {
 'Hamura', 'Chofu', 'Arakawa', 'Inagi', 'Akishima', 'Komae', 'Kodaira', 'Nishitama', 'Sumida', 'Nishitokyo', 'Minato',
 'Koganei', 'Mitaka', 'Higashimurayama', 'Machida', 'Fuchu', 'Kunitachi', 'Shinagawa', 'Ome', 'Meguro', 'Ota',
 'Katsushika', 'Hachioji', 'Musashimurayama', 'Higashiyamato', 'Kiyose', 'Setagaya', 'Chiyoda', 'Edogawa', 'Kokubunji',
 'Akiruno', 'Adachi', 'Taito', 'Tama', 'Tokyo', 'Bunkyo', 'Suginami', 'Higashikurume', 'Shinjuku', 'Nerima', 'Kita',
 'Musashino', 'Toshima', 'Shibuya', 'Koto', 'Tachikawa', 'Itabashi', 'Hino', 'Chuo', 'Fussa', 'Nakano', 'Odawara',
 'Ebina', 'Hiratsuka', 'Atsugi', 'Yamato', 'Chigasaki', 'Sagamihara', 'Kawasaki', 'Hadano', 'Aiko', 'Zushi', 'Miura',
 'Kamakura', 'Ashigarashimo', 'Ayase', 'Isehara', 'Ashigarakami', 'Kanagawa', 'Yokosuka', 'Yokohama', 'Fujisawa',
 'Zama', 'Minamiashigara', 'Koza', 'Naka', 'Asahi', 'Ichikawa', 'Katori', 'Sosa', 'Katsura', 'Narita', 'Isumi', 'Noda',
 'Imba', 'Abiko', 'Urayasu', 'Oamishirasato', 'Yotsukaido', 'Sammu', 'Shiroi', 'Kamagaya', 'Sambu', 'Tateyama',
 'Kisarazu', 'Kamogawa', 'Sakura', 'Choshi', 'Awa', 'Inzai', 'Nagareyama', 'Mobara', 'Minamiboso', 'Matsudo', 'Chiba',
 'Tomisato', 'Narashino', 'Futtsu', 'Yachiyo', 'Chosei', 'Kashiwa', 'Sodegaura', 'Kimitsu', 'Funabashi', 'Ichihara',
 'Yachimata', 'Togane', 'Warabi', 'Saitama', 'Wako', 'Tsurugashima', 'Shiki', 'Osato', 'Iruma', 'Hasuda', 'Asaka',
 'Koshigaya', 'Shiraoka', 'Satte', 'Fujimino', 'Kumagaya', 'Kasukabe', 'Misato', 'Gyoda', 'Okegawa', 'Kitamoto',
 'Sayama', 'Kitakatsushika', 'Yashio', 'Fujimi', 'Minamisaitama', 'Kitadachi', 'Tokorozawa', 'Hiki', 'Toda', 'Kawagoe',
 'Konosu', 'Honjo', 'Hidaka', 'Soka', 'Yoshikawa', 'Sakado', 'Niza', 'Fukaya', 'Kodama', 'Ageo', 'Hanyu',
 'Higashimatsuyama', 'Chichibu', 'Kawaguchi', 'Kazo', 'Hanno', 'Kuki'
}

# 防重复提私钥
ENCRYPTION_PKEY = 'M9M7gXbwhupJ'
# 有效时间, 单位毫秒
ENCRYPTION_TIMEDELTA = 60000
# TODO: XXX
ENCRYPTION_KEY = 'HTTP_X_JYZD'


def verify_request_encryption(request, redis_pool):
    """
    校验写接口,防止重复提交. True 为通过验证, False 为没有通过.
    :type request: django.http.HttpRequest
    :type redis_pool: redis.ConnectionPool
    :rtype: bool
    """
    encrypted_data = request.META.get(ENCRYPTION_KEY, '')
    # 如果加密数据为空, 则返回无效
    if is_blank(encrypted_data):
        return False, 'Empty data'

    # 解出加密数据,如果解数据出错,则返回无效
    try:
        data = base64.b64decode(encrypted_data)
        data = rncryptor.decrypt(data, ENCRYPTION_PKEY)
        timestamp, udid = data.split()
        timestamp = int(timestamp)
    except Exception as e:
        return False, 'Error data, {}'.format(e)

    # 验证时间, 如果当前时间比
    now_ts = int(time.time() * 1000)
    if now_ts > timestamp + ENCRYPTION_TIMEDELTA or now_ts < timestamp - ENCRYPTION_TIMEDELTA:
        return False, 'Invalid time, now={}, args={}, {}, date={}'.format(now_ts, timestamp, udid, encrypted_data)

    try:
        redis_db = redis.StrictRedis(connection_pool=redis_pool)
        key = '{}_{}'.format(udid, timestamp)
        if redis_db.exists(key):
            return False, 'Repeat request, now={}, args={}, {}, date={}'.format(now_ts, timestamp, udid, encrypted_data)

        redis_db.set(key, '1', px=ENCRYPTION_TIMEDELTA)
        return True, 'Success'
    except Exception as e:
        # 降级逻辑, REDIS 挂掉, 默认不进行校验.
        return True, 'Redis error, {}'.format(e)


def is_request_legal(request):
    # todo: use a better way to verify
    return True
    fmek = request.GET.get('fmek', '')
    fmev = request.GET.get('fmev', '')
    if not (fmek and fmev):
        return False
    return md5(fmek + 'justgivemeareason').hexdigest().lower() == fmev


class QueryStr(BaseTypes):
    PHONE_TYPE_IPHONE = 'iphone'
    PHONE_TYPE_ANDROID = 'android'


def is_in_review(app_name, version, phone_type=QueryStr.PHONE_TYPE_IPHONE, geo='jpn', unique_device_id='', app_id=''):
    return False


def is_should_trace(
    unique_device_id, app_name, version, phone_type=QueryStr.PHONE_TYPE_IPHONE,
    geo='jpn',
        ):
    return False


def is_should_block(
    app_name, geo, user_agent
        ):
    if 'okhttp' in user_agent:
        return True
    if 'python' in user_agent:
        return True
    return False


def is_spec_0(mj):
    """
    Spec0: 标识 admob 特殊版本用户
    :param mj:
    :return:
    """
    if mj == '1':
        return True
    return False


def get_geo_country_code3(request):
    '''
        优先读取COUNTRY_CODE，再读取GEOIP_COUNTRY_CODE3
        返回：
            GEO COUNTRY CODE3
    '''
    try:
        if request.META.get('REMOTE_ADDR', '').startswith('17.'):
            return 'usa'
        geo_code_2 = request.META.get('COUNTRY_CODE', '')
        return countries.get(geo_code_2.lower()).alpha3.lower()
    except:
        return request.META.get('GEOIP_COUNTRY_CODE3', '').lower()


def parse_query_str(request):
    '''
        获得 query 中的参数，方便 api 调用。
        对公共的部分进行解析，解决多个 api 需要重复代码的问题。
    '''
    version = request.GET.get("v", "0")
    version_code = int(request.GET.get('version_code', 0))
    app_name = request.GET.get("appname", "").lower()
    phone_type = request.GET.get("phonetype", "iphone").lower()
    app_id = request.GET.get("appid", "")
    device_id = request.GET.get('deviceid', "")
    unique_device_id = request.GET.get('unique_device_id', "")
    os_version = request.GET.get('osv', "")
    device_type = request.GET.get('device_type', "")
    geo = get_geo_country_code3(request)
    ip = request.META.get('REMOTE_ADDR', '')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    in_review = is_in_review(
        app_name, version, phone_type, geo, unique_device_id=unique_device_id, app_id=app_id,
        )
    should_block = is_should_block(
        app_name, geo, user_agent
        )
    should_trace = is_should_trace(
        unique_device_id, app_name, version, phone_type,
        geo)
    lang = translate_lang_from_request(request)
    skin = request.GET.get('skin', '')
    city = request.META.get('CITY_NAME', '') or '-'

    # AB 测试标识
    e_flag = request.GET.get('e_flag', '')
    #e_flag = urlparse(e_flag)
    # 日本城市jis code
    city_code = request.GET.get('city_code', '')
    access = request.GET.get('access', 'unknown')
    idfa = request.GET.get('idfa', '')
    query = dict((
        ('version', version),
        ('version_code', version_code),
        ('app_name', app_name),
        ('app_id', app_id),
        ('lang', lang),
        ('phone_type', phone_type),
        ('device_id', device_id),
        ('unique_device_id', unique_device_id),
        ('os_version', os_version),
        ('geo', geo),
        ('ip', ip),
        ('device_type', device_type),
        ('user_agent', user_agent),
        ('in_review', in_review),
        ('should_block', should_block),
        ('should_trace', should_trace),
        ('skin', skin),
        ('city', city),
        ('is_tokyo', city in TOKYO_CITIES),
        ('e_flag', e_flag),
        ('city_code', city_code),
        ('access', access),
        ('idfa', idfa),
        ))
    return QueryStr(query)


def parse_query_str_dict(request):
    result = dict(request.GET.iterlists())
    for k, v in result.items():
        if isinstance(v, list):
            v = ','.join(v)
        result[k] = v.encode('utf8')
    return result


def is_android_outcast(unique_device_id):
    # 空的设备udid不进审
    if is_blank(unique_device_id):
        return False
    # 不合格的udid进审
    if len(unique_device_id) < 23:
        return True
    ts = int(unique_device_id[:17])
    # 2018-07-23 22:00:00
    if ts > 15323544000000000:
        return True
    return False
