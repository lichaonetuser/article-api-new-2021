# coding=utf-8
import functools
import random
import redis
from mongoengine import Q

from pyutil.text.conv import is_blank
from pyutil.api.redis_key import get_user_message_count, get_device_push_group_count
from api.settings import redis_pool
from api.inbox.constants import OLD_MESSAGE_NORMAL, NOTIFICATION_GROUP, GROUP_MATCH
from api.inbox.constants import ACTION_PUSH_PROFILE, ACTION_PUSH_SUBGROUP
from api.inbox.models import MessageOldStage, NotificationInbox


class InboxDAL(object):

    def __init__(self, ):
        self.write_redis = redis.StrictRedis(connection_pool=redis_pool["message_write"])
        # TODO redis有主从时，考虑message_read独立配置
        self.read_redis = redis.StrictRedis(connection_pool=redis_pool["message_write"])

    def message_load(self, pk, last_id, limit):
        if is_blank(pk):
            return [], False

        kwargs = {
            'to_uid': pk,
            'status': OLD_MESSAGE_NORMAL,
        }

        if not is_blank(last_id):
            kwargs['pk__lt'] = last_id

        rs = MessageOldStage.objects(**kwargs).order_by('-id').limit(limit + 1)

        comments = [item for item in rs]
        has_more = False
        if len(comments) > limit:
            has_more = True
            comments = comments[:limit]

        return comments, has_more

    def push_load(self, phone_type, udid, last_id, limit):
        if is_blank(udid):
            return [], False

        # 取出分组(ios/android)推送、个性化推送记录
        group_id = NOTIFICATION_GROUP.get(phone_type, 1)
        query = Q(group_id=group_id, target_id__ne='')
        if not is_blank(last_id):
            query = query & Q(pk__lt=last_id)
        items = list(NotificationInbox.objects(query).order_by('-id').limit(limit + 1))

        final_text_items = []
        if not is_blank(udid):
            # TODO embeded document optimize
            profile_item = NotificationInbox.objects(udid=udid, action_type=ACTION_PUSH_PROFILE).first()
            if profile_item:
                items.insert(0, profile_item)

            udid_text_item = NotificationInbox.objects(udid=udid, action_type=ACTION_PUSH_SUBGROUP).first()
            if udid_text_item:
                udid_text_nids = {x.target_id: x.notification_id for x in udid_text_item.target_items}
                query = Q(group_id=GROUP_MATCH, action_type=ACTION_PUSH_SUBGROUP)
                if last_id:
                    query = query & Q(pk__lt=last_id)
                text_items = {x.notification_id: x for x in list(NotificationInbox.objects(query).order_by('-id').limit(limit + 1))}
                for tid, nid in udid_text_nids.items():
                    if nid in text_items:
                        text_items[nid].target_id = tid
                        final_text_items.append(text_items[nid])

        items = self.filter_group_for_profile(udid, items)
        items.extend(final_text_items)
        items = sorted(items, key=functools.cmp_to_key(lambda x, y: int((y.ctime - x.ctime).total_seconds())))
        has_more = False
        if len(items) > limit:
            has_more = True
            items = items[:limit]

        return items, has_more

    def filter_group_for_profile(self, udid, items):
        group_items = []
        profile_items = {}
        for x in items:
            if x.udid == udid:
                profile_items = {x.notification_id: x.target_id for x in x.target_items}
            else:
                group_items.append(x)

        res_items = []
        for x in group_items:
            if x.notification_id in profile_items:
                # 需要把group item的pk/ctime返回出去，用于last_id的比较判断与display_time
                item = NotificationInbox(target_id=profile_items[x.notification_id], target_type=4, pk=x.pk, ctime=x.ctime)
                res_items.append(item)
            else:
                res_items.append(x)

        return res_items

    # @read_balance
    def _get_redis_value(self, key, idx=0):
        redis_db = self.read_redis
        return redis_db.get(key) or '0'

    def get_user_message_count(self, uid):
        return int(self._get_redis_value(get_user_message_count(uid)))

    def clear_user_message_count(self, uid):
        if is_blank(uid):
            return
        self.write_redis.set(get_user_message_count(uid), '0')

    def get_device_push_group_count(self, group_id, udid):
        return int(self._get_redis_value(get_device_push_group_count(group_id, udid)))

    def set_device_push_group_count(self, group_id, udid, val):
        if is_blank(udid):
            return
        self.write_redis.set(get_device_push_group_count(group_id, udid), val)
