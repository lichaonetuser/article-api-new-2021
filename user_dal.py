import redis
import time
import json
from datetime import datetime
from api.user.constants import INVALID_IDFAS
from api.constants import EnumUserGroup
from api.log import exception_logger, api_logger

from api.user.models import UserSelectInfo, UniqueDeviceInfo
from pyutil.api.redis_key import get_songlist_receive_version_for_udid_key, \
    get_songlist_receive_version_key, get_uid_info_key
from pyutil.api.account import Platform
from api.user.types import MAX_DEVICES_ONLINE, LoginStatus, User
from api.channel.constants import VALID_GENDERS, VALID_AGES

class UniqueDeviceInfoDAL(object):
    def __init__(self, redis_pool):
        self.udid_status_redis = redis.StrictRedis(connection_pool=redis_pool)

    @staticmethod
    def get_udid_by_idfa(idfa):
        if not idfa or idfa in INVALID_IDFAS or len(set(idfa)) < 5:
            api_logger.error('invalid idfa:{}'.format(idfa))
            return None
        records = list(UniqueDeviceInfo.objects(idfa=idfa))
        if records and len(records[0].unique_device_id) > 10:
            api_logger.info('get_udid_by_idfa succeed|idfa:{}|udid:{}'.format(idfa, records[0].unique_device_id))
            return records[0].unique_device_id
        return None

    @staticmethod
    def set_udid_by_idfa(idfa, udid, e_flag=''):
        # 统计要求，无效idfa统一置为空存储
        if not idfa or idfa in INVALID_IDFAS or len(set(idfa)) < 5:
            api_logger.error('invalid idfa:{}|udid:{}'.format(idfa, udid))
            idfa = ''
        device_info = UniqueDeviceInfo.objects(unique_device_id=udid, idfa=idfa).first()
        if device_info is None:
            device_info = UniqueDeviceInfo(idfa=idfa, unique_device_id=udid)
            if e_flag:
                device_info.e_flag = e_flag
            device_info.save()
            api_logger.info('idfa:{}|udid:{}'.format(idfa, udid))

    @staticmethod
    def set_udid_by_atd(atd, udid, e_flag=''):
        # 统计要求，无效atd统一置为空存储
        if not atd or len(set(atd)) < 5:
            api_logger.error('invalid atd:{}|udid:{}'.format(atd, udid))
            atd = ''
        device_info = UniqueDeviceInfo.objects(unique_device_id=udid, atd=atd).first()
        if device_info is None:
            device_info = UniqueDeviceInfo(unique_device_id=udid, atd=atd)
            if e_flag and UniqueDeviceInfo.objects(unique_device_id=udid, e_flag__exists=1).first() is None:
                device_info.e_flag = e_flag
            device_info.save()
            api_logger.info('atd:{}|udid:{}'.format(atd, udid))

    @staticmethod
    def set_udid_by_afid(af_id, udid):
        if not af_id:
            api_logger.error('invalid af_id:{}'.format(af_id))
            return
        device_info = UniqueDeviceInfo.objects(unique_device_id=udid).first()
        if device_info:
            device_info.af_id = af_id
        else:
            device_info = UniqueDeviceInfo()
            device_info.unique_device_id = udid
            device_info.af_id = af_id
        device_info.save()
        api_logger.info('af_id:{}|udid:{}'.format(af_id, udid))

    def get_udid_status(self, udid, atd):
        udid_status = EnumUserGroup.ALL
        try:
            udid_ctime = int(self.udid_status_redis.get(udid) or time.time())
            tstruct0 = datetime.now().timetuple()
            tstruct1 = time.localtime(udid_ctime)
            if tstruct0.tm_year == tstruct1.tm_year and tstruct0.tm_yday == tstruct1.tm_yday:
                udid_status = EnumUserGroup.NEW
                # 新用户考虑存入atd
                if atd:
                    UniqueDeviceInfoDAL.set_udid_by_atd(atd, udid)
        except Exception as e:
            exception_logger.exception('udid:{} except:{}'.format(udid, e))

        return udid_status

    def set_udid_ts(self, udid):
        try:
            self.udid_status_redis.setnx(udid, int(time.time()))
        except Exception as e:
            exception_logger.exception('udid:{}, e:{}'.format(udid, e))

    def get_udid_ts(self, udid):
        return bool(self.udid_status_redis.get(udid))


class UserDAL():

    def clear_device(self, uid, udid, uid_info_redis_cli):
        key = get_uid_info_key(uid)
        raw_online_devices = uid_info_redis_cli.hget(key, 'online_devices')
        online_devices = json.loads(raw_online_devices) \
            if raw_online_devices else []
        online_devices = [_udid for _udid in online_devices if _udid != udid]
        if online_devices:
            uid_info_redis_cli.hset(
                key, 'online_devices', json.dumps(online_devices))
        else:
            uid_info_redis_cli.delete(key)

    def get_login_status(
        self, token_expire_at, uid, udid, platform, redis_cli
    ):
        if token_expire_at < int(time.time()):
            if platform == Platform.FACEBOOK:
                login_status = LoginStatus.FACEBOOK_TOKEN_EXPIRE
            elif platform == Platform.TWITTER:
                login_status = LoginStatus.TWITTER_TOKEN_EXPIRE
            else:
                login_status = LoginStatus.UNKNOWN_EXPIRE
        else:
            key = get_uid_info_key(uid)
            raw_online_devices = redis_cli.hget(key, 'online_devices')
            online_devices = json.loads(raw_online_devices) \
                if raw_online_devices else []
            if udid in online_devices:
                login_status = LoginStatus.OK
            else:
                login_status = LoginStatus.FORCE_LOGOUT
        return login_status

    def save_uid_online_devices(self, uid, udid, redis_cli):
        key = get_uid_info_key(uid)
        raw_online_devices = redis_cli.hget(key, 'online_devices')
        online_devices = json.loads(raw_online_devices) \
            if raw_online_devices else []
        if udid not in online_devices:
            online_devices.append(udid)
        online_devices = online_devices[-MAX_DEVICES_ONLINE:]
        redis_cli.hset(key, 'online_devices', json.dumps(online_devices))

    def get_songlist_cvs(self, uid, udid, redis_cli):
        if uid:
            id, id_type = uid, User.TYPE_UID
        else:
            id, id_type = udid, User.TYPE_UNIQUE_DEVICE_ID
        cvs_key = get_songlist_receive_version_key(id, id_type)
        version_info = redis_cli.get(cvs_key)
        version_key = get_songlist_receive_version_for_udid_key(udid)
        version_info = {} if not version_info else eval(version_info)
        csv = int(version_info.get(version_key, -1))
        return csv


class UserSelectInfoDAL(object):
    def __init__(self):
        pass

    @staticmethod
    def get(udid, uid):
        pk, utype = (uid, 1) if uid else (udid, 0)
        try:
            user_select_info = UserSelectInfo.objects.get(user_id=pk, user_type=utype)
            user_select_info_dict = dict(gender=user_select_info.gender, age_stage=user_select_info.age_stage)
            return user_select_info_dict
        except Exception as e:
            pass
        return {}

    @staticmethod
    def set(udid, gender, age_stage, uid):
        pk, utype = (uid, 1) if uid else (udid, 0)
        # 性别、年龄需至少存在一个有效信息
        if gender not in VALID_GENDERS and age_stage not in VALID_AGES:
            raise Exception('udid={}|invalid gender={}|age={}'.format(udid, gender, age_stage))

        if gender == -1:
            rv = UserSelectInfo.objects(user_id=pk, user_type=utype).modify(age_stage=age_stage, mtime=datetime.now(), upsert=True, new=True)
        elif age_stage == -1:
            rv = UserSelectInfo.objects(user_id=pk, user_type=utype).modify(gender=gender, mtime=datetime.now(), upsert=True, new=True)
        else:
            rv = UserSelectInfo.objects(user_id=pk, user_type=utype).modify(gender=gender, age_stage=age_stage, mtime=datetime.now(), upsert=True, new=True)
        return {'gender': rv.gender, 'age_stage': rv.age_stage}


class UniqueDeviceInfoDAL(object):
    def __init__(self, redis_pool):
        self.udid_status_redis = redis.StrictRedis(connection_pool=redis_pool)

    @staticmethod
    def get_udid_by_idfa(idfa):
        if not idfa or idfa in INVALID_IDFAS or len(set(idfa)) < 5:
            api_logger.error('invalid idfa:{}'.format(idfa))
            return None
        records = list(UniqueDeviceInfo.objects(idfa=idfa))
        if records and len(records[0].unique_device_id) > 10:
            api_logger.info('get_udid_by_idfa succeed|idfa:{}|udid:{}'.format(idfa, records[0].unique_device_id))
            return records[0].unique_device_id
        return None

    @staticmethod
    def set_udid_by_idfa(idfa, udid, e_flag=''):
        # 统计要求，无效idfa统一置为空存储
        if not idfa or idfa in INVALID_IDFAS or len(set(idfa)) < 5:
            api_logger.error('invalid idfa:{}|udid:{}'.format(idfa, udid))
            idfa = ''
        device_info = UniqueDeviceInfo.objects(unique_device_id=udid, idfa=idfa).first()
        if device_info is None:
            device_info = UniqueDeviceInfo(idfa=idfa, unique_device_id=udid)
            if e_flag:
                device_info.e_flag = e_flag
            device_info.save()
            api_logger.info('idfa:{}|udid:{}'.format(idfa, udid))

    @staticmethod
    def set_udid_by_atd(atd, udid, e_flag=''):
        # 统计要求，无效atd统一置为空存储
        if not atd or len(set(atd)) < 5:
            api_logger.error('invalid atd:{}|udid:{}'.format(atd, udid))
            atd = ''
        device_info = UniqueDeviceInfo.objects(unique_device_id=udid, atd=atd).first()
        if device_info is None:
            device_info = UniqueDeviceInfo(unique_device_id=udid, atd=atd)
            if e_flag and UniqueDeviceInfo.objects(unique_device_id=udid, e_flag__exists=1).first() is None:
                device_info.e_flag = e_flag
            device_info.save()
            api_logger.info('atd:{}|udid:{}'.format(atd, udid))

    @staticmethod
    def set_udid_by_afid(af_id, udid):
        if not af_id:
            api_logger.error('invalid af_id:{}'.format(af_id))
            return
        device_info = UniqueDeviceInfo.objects(unique_device_id=udid).first()
        if device_info:
            device_info.af_id = af_id
        else:
            device_info = UniqueDeviceInfo()
            device_info.unique_device_id = udid
            device_info.af_id = af_id
        device_info.save()
        api_logger.info('af_id:{}|udid:{}'.format(af_id, udid))

    def get_udid_status(self, udid, atd):
        udid_status = EnumUserGroup.ALL
        try:
            udid_ctime = int(self.udid_status_redis.get(udid) or time.time())
            tstruct0 = datetime.now().timetuple()
            tstruct1 = time.localtime(udid_ctime)
            if tstruct0.tm_year == tstruct1.tm_year and tstruct0.tm_yday == tstruct1.tm_yday:
                udid_status = EnumUserGroup.NEW
                # 新用户考虑存入atd
                if atd:
                    UniqueDeviceInfoDAL.set_udid_by_atd(atd, udid)
        except Exception as e:
            exception_logger.exception('udid:{} except:{}'.format(udid, e))
        return udid_status

    def set_udid_ts(self, udid):
        try:
            self.udid_status_redis.setnx(udid, int(time.time()))
        except Exception as e:
            exception_logger.exception('udid:{}, e:{}'.format(udid, e))

    def get_udid_ts(self, udid):
        return bool(self.udid_status_redis.get(udid))


