# coding=utf-8
from __future__ import absolute_import
from api.constants import EnumChannelType, SHARE_URL
from api.constants import EnumItemType
from api.constants import EnumLanguageType
from api.constants import EnumListItemStyle
from api.constants import EnumVideoSourceType
from api.constants import EnumActive
from api.log import exception_logger
from pyutil.text.conv import is_blank
from api.utils.api import APIModel
from api.utils.encoding import encrypt_id, DATA_TYPE_ARTICLE
from api.utils.media import extract_medias, MediaVideo
from api.utils.model import SourceMixin, ActionMixin, FeedItemMixin
from api.utils.time_util import try_parse_datetime_ts
from api.video.constants import DEFAULT_YOUTUBE_ICON


class Video(APIModel, SourceMixin, ActionMixin, FeedItemMixin):
    def __init__(self, data=None):
        super(Video, self).__init__()
        SourceMixin.__init__(self)
        ActionMixin.__init__(self)
        FeedItemMixin.__init__(self)
        self.id = 0
        self.item_id = 0
        self.title = ''
        self.y_video_id = ''
        self.description = ''
        self.cover_image = ''
        self.duration_interval = 0
        self.published_at = 0
        self.share_url = ''
        self.type = EnumItemType.VIDEO
        self.cover_image_urls = []

        self.source_type = EnumVideoSourceType.YOUTUBE
        self.style = EnumListItemStyle.VIDEO_PLAYABLE
        # source 相关字段, 数据提供原始字段
        self.channel_name = ''
        self.avatar_url = ''

        self.medias = []

        self.sd_url = ''
        self.normal_url = ''
        self.hd_url = ''
        self.original_site_url = ''
        self.is_active = EnumActive.ENABLE
        # FIXME 不一致的一个字段
        self.comment_count = 0
        self.language = EnumLanguageType.UNKNOWN
        self.likes = 0
        self.dislikes = 0
        self.init(data)
        self.id = self.item_id
        self.aid = encrypt_id(DATA_TYPE_ARTICLE, self.item_id)

    def normalize(self, query_str):
        if self.is_active == EnumActive.DISABLE:
            return None
        if self.language != EnumLanguageType.JA:
            self.title = ''
        if not isinstance(self.published_at, int):
            self.published_at = try_parse_datetime_ts(self.published_at)
        # 视频是youtube视频时需要处理的数据
        if self.source_type == EnumVideoSourceType.YOUTUBE:
            self.original_site_url = 'https://www.youtube.com/watch?v={}'.format(self.y_video_id)
            self.source_name = 'Youtube' if is_blank(self.channel_name) else self.channel_name
            self.source_pic = DEFAULT_YOUTUBE_ICON if is_blank(self.avatar_url) else self.avatar_url

        # 如果source_type是URL的, 需要从media中抽取相应的数据
        if self.source_type == EnumVideoSourceType.URL and self.medias:
            medias = extract_medias(self.medias, logger=exception_logger)
            if medias:
                v = medias[0]
                if not isinstance(v, MediaVideo):
                    raise ValueError('video[mp4] has invalid format.{}'.format(v))
                self.__dict__.update(v.get_urls())
                self.duration_interval = v.duration

            if self.cover_image_urls:
                self.cover_image = self.cover_image_urls[0]
            self.style = EnumListItemStyle.VIDEO_PLAYABLE
            self.source_pic = self.avatar_url

        if hasattr(query_str, 'channel_type'):
            if query_str.channel_type == EnumChannelType.ARTICLE:
                self.style = EnumListItemStyle.VIDEO_LARGE_COVER

        # 客户端需要type始终为1, 数据端可能有很多类型都是video
        self.type = EnumItemType.VIDEO
        self.share_url = SHARE_URL.format(self.type, self.aid)
        return self

    def has_copyright(self):
        return True

    def as_dict(self):
        t = dict(self.__dict__)
        del t['id']
        del t['item_id']
        del t['likes']
        del t['dislikes']
        del t['medias']
        del t['manual_tags']
        return t
