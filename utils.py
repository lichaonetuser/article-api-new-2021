# coding=utf-8
from __future__ import absolute_import

from api.article.constants import SESSION_KEY_USER_PREF
from api.utils.collection import stringify_dict_values


def emit_check(article_dict, ctx):
    """
    检查文章能否在当前上下中下放出
    :type article_dict: dict
    :type ctx: dict
    :rtype: bool
    """
    return True


def build_recsys_params(uid, query_str, session=None):
    """
    构建推荐通用参数
    :param uid:
    :param query_str:
    :return:
    """
    ret = {'uid': uid}
    stringify_dict_values(query_str.__dict__, ret)

    if session:
        user_pref = session.get(SESSION_KEY_USER_PREF, {})
        if user_pref:
            # 与推荐约定，非有效值则不传key参数
            if user_pref.get('gender', -1) == -1:
                user_pref.pop('gender', None)
            if user_pref.get('age_stage', -1) == -1:
                user_pref.pop('age_stage', None)
            stringify_dict_values(user_pref, ret)
    return ret
