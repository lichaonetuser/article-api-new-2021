# coding=utf-8
import os
import datetime
from pyutil.program.conf import Conf

auth_conf = Conf(os.path.join(os.path.dirname(__file__), 'conf/auth.conf'))

from pyutil.user.account.types import Account

local_host = auth_conf.get_values('thrift_auth_host')
local_port = auth_conf.get_values('thrift_new_auth_port')


def format_return_user(user):
    if 'user' in user:
        user_obj = user.get('user', None)
        user = user_obj.__dict__ if (user_obj and user_obj.uid) else {}
    return user


def login(platform, *args, **kwargs):
    '''
    #thrift取消，改为微服务2020-12-28
    host = kwargs.get("host", local_host)
    port = kwargs.get("port", local_port)
    client = Login(host=host, port=port)
    device_status, query_str = {}, kwargs.get('query_str', None)
    if query_str:
        device_status['unique_device_id'] = query_str.unique_device_id
        device_status['geo'] = query_str.geo
        device_status['app_id'] = query_str.app_id
        device_status['app_version'] = query_str.version
        device_status['online_status'] = 1
        device_status['ctime'] = str(datetime.datetime.now())
        device_status['last_login_time'] = str(datetime.datetime.now())
        device_status['phone_type'] = \
            0 if 'iphone' in query_str.phone_type else 1
        device_status['extra_info'] = query_str.__dict__
    del_keys = ["query_str", "host", "port"]
    for key in del_keys:
        if key in kwargs:
            del kwargs[key]
    kwargs['device_status'] = device_status
    req = LoginReq(platform, **kwargs)
    status, result, msg = client.process(req)
    user = format_return_user(result)
    user['is_fresh'] = result['is_fresh']
    return status, user, msg
    '''
    return {}

def sync(uid, **kwargs):

    return {}


def get_account_info(uid, **kwargs):
    return {}


def logout(uid, unique_device_id='', app_id='', query_str=None, **kwargs):
    return {}

def get_uid_by_udid(udid, **kwargs):
    return {}


def update(user_profile, **kwargs):
    return {}


def users(uids, **kwargs):
    return {}


def pusic_regist(*args, **kwargs):
    return {}
