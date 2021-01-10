# coding=utf8
import re


def translate_lang_from_request(request):
    channel_lang = request.GET.get('channel_lang', '').lower()
    lang = request.GET.get('lang', '').lower()
    lang = channel_lang or lang
    return translate_lang(lang)


def translate_lang(lang):
    if re.search('^ja*', lang):
        return 'ja'
    elif re.search('^(zh-hant|zh-HK|zh-TW)', lang):
        return 'zh-hant'
    elif re.search('^(zh-hans*|zh)', lang):
        return 'zh-hans'
    elif re.search('^ko*', lang):
        return 'ko'
    elif re.search('^test*', lang):
        return 'test'
    else:
        return 'en'

