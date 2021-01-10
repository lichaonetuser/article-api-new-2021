# coding=utf-8
import json
from urllib.parse import urlparse

import time

import redis
from api.log import exception_logger
from pyutil.text.conv import is_blank

VIDEO_HOTLINK_REDIS_KEY = 'vh_{}'
VIDEO_HOTLINK_QUEUE_KEY = 'video_hotlink_q'


def _get_expires_from_url(url):
    if not url:
        return 0
    qs = urlparse.urlparse(url)
    if 'expire' not in qs or not qs['expire']:
        return 0
    return int(qs['expire'][0])


class VideoDAL(object):
    def __init__(self, redis_pool):
        self.cli = redis.StrictRedis(connection_pool=redis_pool)

    def urls(self, y_video_ids):
        ret = {}
        try:
            with self.cli.pipeline() as p:
                for yid in y_video_ids:
                    p.get(VIDEO_HOTLINK_REDIS_KEY.format(yid))
                rs = p.execute()
            items = zip(y_video_ids, rs)
            for item in items:
                try:
                    if item[1]:
                        ret[item[0]] = json.loads(item[1])
                except:
                    exception_logger.exception('VideoDAL.urls()_json_err:{}'.format(y_video_ids))
        except:
            exception_logger.exception('VideoDAL.urls()_err')
        return ret

    def report(self, y_video_id, url_dict):
        if not url_dict:
            return
        k = VIDEO_HOTLINK_REDIS_KEY.format(y_video_id)
        r = self.cli.exists(k)
        if not r:
            expire = _get_expires_from_url(url_dict.values()[0])
            if expire == 0:
                return
            now_ts = int(time.time())
            self.cli.set(k, json.dumps(url_dict), ex=expire - now_ts)


class VideoHotlinkDAL(object):
    def __init__(self, redis_pool):
        self.cli = redis.StrictRedis(connection_pool=redis_pool)

    def queue_jump(self, y_video_id):
        """
        由于更新环是rpush-blpop的顺序, 所以使用lpush插队,可以让y_video_id能够进到队列头部, 提前盗链
        :param y_video_id:
        :return:
        """
        try:
            if is_blank(y_video_id):
                return
            self.cli.lpush(VIDEO_HOTLINK_QUEUE_KEY, '*_{}'.format(y_video_id))
        except:
            exception_logger.exception('video_hotlink_queue_jump_err: {}'.format(y_video_id))
