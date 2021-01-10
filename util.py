# coding=utf-8
import json

from api.comment.constants import TARGET_TYPE_LITERAL_MAP
from api.log import exception_logger


def inc_count_in_cache(cache_obj, key, step, *args, **kwargs):
    """
    考虑性能, 将计数器同步的在mc中增加. 考虑解耦, 没有放进dal中.
    :param key:
    :param step:
    :return:
    """
    n = abs(step)
    v = cache_obj.get_cache_data(key, *args, **kwargs)
    if v:
        if step > 0:
            for i in range(n):
                cache_obj.incr(key, *args, **kwargs)
        else:
            for i in range(n):
                cache_obj.decr(key, *args, **kwargs)
    else:
        if step > 0:
            cache_obj.set_cache_data(key, step, 0, *args, **kwargs)


def set_comment_target(comments):
    """
    只有在sport board中使用
    :type comments: list[dict]
    :return:
    """
    for comment in comments:
        if '_snap_target' in comment and comment['_snap_target'] and comment['target_type'] in TARGET_TYPE_LITERAL_MAP:
            try:
                m = json.loads(comment['_snap_target'])
                # 由于客户端对象缓存池的原因, 快照时会变的状态应该在返回时去掉, 避免影响客户端状态.
                if 'game_status' in m:
                    del m['game_status']
                if 'home_team' in m:
                    if 'point_sphere' in m['home_team']:
                        del m['home_team']['point_sphere']
                    if 'score' in m['home_team']:
                        del m['home_team']['score']
                if 'away_team' in m:
                    if 'point_sphere' in m['away_team']:
                        del m['away_team']['point_sphere']
                    if 'score' in m['away_team']:
                        del m['away_team']['score']
                comment[TARGET_TYPE_LITERAL_MAP[comment['target_type']]] = m
                del comment['_snap_target']
            except:
                exception_logger.exception('_set_comment_target: comment={}'.format(comment))
    return comments
