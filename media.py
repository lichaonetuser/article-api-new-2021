# coding=utf-8
"""
根据数据组的media数据,抽出需要的数据.
XXX 有一些和表名关联逻辑, 重构或者修改表名时, 需要十分注意.
"""


class _EnumVideoResolution:
    LOW = '0'
    MEDIUM = '1'
    HIGH = '2'


class _EnumMessageType:
    """
    数据端使用的常量,原则上API不应该使用
    """
    TWITTER_IMAGE = 2
    GIF = 3
    TWITTER_VIDEO = 4


# 以下均为标识类型
class MediaImage:
    def __init__(self, data):
        self.data = data

    def format(self, use_cdn=False):
        return {
            'width': self.data.get('ori_width', 0),
            'height': self.data.get('ori_height', 0),
            'urls': [self.cdn_url(self.data.get('path', '')), ]
        }


class MediaGIFVideo:
    def __init__(self, data):
        self.data = data

    def format(self, use_cdn=False):
        ret = {
            'width': self.data.get('width', 0),
            'height': self.data.get('height', 0),
            'urls': [self.data['url'], ],
            'duration': self.data.get('duration', 0),
            'kps': self.data.get('kps', 0)
        }
        return ret


class MediaGIFImage:
    def __init__(self, data):
        self.data = data

    def format(self, use_cdn=False):
        ret = {
            'width': self.data.get('width', 0),
            'height': self.data.get('height', 0),
            'urls': [self.data['url'], ]
        }
        return ret


class MediaVideo:
    RESOLUTION_MAP = {'0': 'sd_url', '1': 'normal_url', '2': 'hd_url'}

    def __init__(self, data):
        self.data = data
        self.duration = 0

    def get_urls(self):
        """
        如果缺值,策略是优先拿高分辨率的来补
        :return:
        """
        r = {}
        default_url = ''
        for k in {'0', '1', '2'}:
            if k in self.data:
                url = self.data[k]['url']
                default_url = url
                r[MediaVideo.RESOLUTION_MAP[k]] = url
                self.duration = self.data[k]['duration']
        # XXX 一个假设, 至少有一个k, 所以default_url肯定有值
        for k in {'sd_url', 'normal_url', 'hd_url'}:
            if k not in r:
                r[k] = default_url
        return r


def extract_medias(medias, logger=None):
    if not medias:
        return []

    ret = []
    for media in medias:
        try:
            if not media:
                continue
            type_ = media['type']
            if type_ == _EnumMessageType.TWITTER_IMAGE:
                ret.append(MediaImage(data=media))
                continue
            if type_ == _EnumMessageType.GIF:
                if media['table'] == 'video':
                    ret.append(MediaGIFVideo(data=media["0"]))
                elif media['table'] == 'image':
                    ret.append(MediaGIFImage(data=media))
                else:
                    raise ValueError('unsupported media table.{}'.format(media['table']))
                continue
            elif type_ == _EnumMessageType.TWITTER_VIDEO:
                ret.append(MediaVideo(data=media))

        except:
            if logger:
                _id = media.get('id', 'None')
                logger.exception('extract_media()_err:id={}'.format(_id))
    return ret
