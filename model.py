# coding=utf-8
from __future__ import absolute_import
from future.utils import lfilter
import json

from future.utils import lmap

from api.constants import EnumListItemStyle, EnumItemType
from api.utils.constants import CS_COMMENT_ENABLE
from api.utils.tag import TAG_HOT, TAG_IMPORTANT, TAG_DISCUSSED, make_sport_tag


class FeedItemMixin(object):
    def __init__(self):
        self.aid = ''
        # 入队时间
        self.emit_time = 0
        # 用来处理Feed中时间的显示逻辑
        self.display_time = 0
        # 显示样式, 文章/视频/.. 统一在一个取值空间
        self.style = EnumListItemStyle.IMAGE_RIGHT
        # 显示控制项
        self.display_options = 0
        # 地域字典
        # - city_name
        # - location_name
        # - city_code
        # - town_name
        self.location = {}
        # 发布时间
        self.published_at = 0

    def has_images(self):
        """
        判断Feed元素是否包含图片
        :return:
        """
        return False


class SourceMixin(object):
    def __init__(self):
        self.copyright_type = 0
        # 版权来源id
        self.copyright_source_id = 0
        # 文章来源id
        self.source_id = 0
        # 文章来源名称
        self.source_name = ''
        # 文章来源图标/商标
        self.source_pic = ''
        # 文章来源聚合id
        self.source_group_id = 0
        # 该版权源下文章是否能够评论
        self.comment_type = CS_COMMENT_ENABLE
        # 一级分类
        self.category_id = 0
        # 二级分类
        self.sub_category_id = 0

    def has_copyright(self):
        return True


class ActionMixin(object):
    def __init__(self):
        # 顶
        self.is_digged = False
        # 踩
        self.is_buried = False
        # 收藏
        self.is_favorite = False
        # 顶数
        self.dig_count = 0
        # 踩数
        self.bury_count = 0
        # 评论数
        self.comment_count = 0
        # 是否热门评论
        self.is_comment_hot = False
        # tags
        self.tags = []
        self.manual_tags = []
        # 数据端传过来的tag数据
        self.tag = ''

    def clear_action_info(self):
        delattr(self, 'is_digged')
        delattr(self, 'is_buried')
        delattr(self, 'is_favorite')
        delattr(self, 'dig_count')
        delattr(self, 'bury_count')
        delattr(self, 'comment_count')
        delattr(self, 'is_comment_hot')
        # delattr(self, 'tags')
        # delattr(self, 'tag')

    def adapt_tags(self):
        """
        适配从数据端来的tag基本信息到客户端需要的数据
        """
        if self.tag and self.tag.strip() != '':
            try:
                tags = json.loads(self.tag)
                is_hot = tags.get('is_hot', False)
                is_important = tags.get('is_important', False)
                is_discussed = tags.get('is_discussed', False)
                if is_hot:
                    self.tags.append(TAG_HOT)
                if is_important:
                    self.tags.append(TAG_IMPORTANT)
                if is_discussed:
                    self.tags.append(TAG_DISCUSSED)
                    self.is_comment_hot = True
                # FIXME 比较别扭的逻辑
                hit_keywords = tags.get('sport_ref', [])
                if hasattr(self, 'type') and self.type == EnumItemType.VIDEO:
                    if hit_keywords:
                        keywords = sorted(hit_keywords, key=lambda x: x[1], reverse=True)
                        self.tags.extend(lmap(lambda x: make_sport_tag(x[0]), keywords[:3]))
                # TODO 要闻后台人工标签逻辑,目前仅实现去掉要闻标签逻辑,其他功能待产品进一步细化
                if self.manual_tags == [0]:
                    self.tags = lfilter(lambda x: x['id'] != TAG_IMPORTANT['id'], self.tags)
            except:
                pass
