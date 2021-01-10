# coding=utf-8
import yaml

DEFAULT_KEY = '_'


class MultilingualTextManager(object):
    """
    多语言文本话术:
    {
        'tag_error': {
            'ja': "の',
            'en': 'of',
            'zh-hans': '的',
            'zh-hant': '的',
            '_': '',
        }
    }
    '_'表示缺省文本.

    >>> MultilingualTextManager().text('tag_error', 'ja')
    """
    def __init__(self, texts):
        assert isinstance(texts, dict)
        self.texts = texts

    def text(self, key, lang, with_default=True):
        ret = self.texts.get(key, {}).get(lang, None)
        if not ret and with_default:
            ret = self.texts.get(key, {}).get(DEFAULT_KEY)
        return ret or ''

    @staticmethod
    def load_from_yaml(path):
        with open(path, 'r', encoding='UTF-8') as fp:
            texts = yaml.load(fp, Loader=yaml.FullLoader) or {}
            return MultilingualTextManager(texts)
