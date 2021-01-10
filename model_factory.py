# coding=utf-8
from __future__ import absolute_import
import json
import logging

from future.utils import lmap

from api.article.models import Article
from api.constants import EnumItemType
from api.video.models import Video
from api.sns_item.models import TwitterImage, GIF, Essay

cls_map = {
    EnumItemType.ARTICLE: Article,
    EnumItemType.VIDEO: Video,
    EnumItemType.IMAGE: TwitterImage,
    EnumItemType.GIF: GIF,
    EnumItemType.TWITTER_VIDEO: Video,
    EnumItemType.ESSAY: Essay,
}


def model_from_json(json_str):
    """
    根据json
    :param json_str:
    :return:
    """
    try:
        data = json.loads(json_str)
        # 兼容逻辑,没有type字段的,默认为文章
        type_ = data.get('type', EnumItemType.ARTICLE)
        return cls_map[type_](data)
    except:
        logging.getLogger('exc').exception('model_from_json: error {}'.format(json_str))
        return None


def model_seq_from_json(seq_of_json_str):
    return lmap(lambda x: model_from_json(x), seq_of_json_str)
