# coding=utf-8
"""
支持客户端emoji自定义图标功能
    - 对于不支持自定义图标功能的android版本,替换成emoji字符
"""
import re

PATTERN = re.compile('\[-(\d+)-\]')

_ID_EMOJI_MAP = dict((
    (0, u'\ud83d\ude0a'),
    (1, u'\ud83d\ude01'),
    (2, u'\ud83d\ude04'),
    (3, u'\ud83d\ude33'),
    (4, u'\ud83d\ude1c'),
    (5, u'\ud83d\ude18'),
    (6, u'\ud83d\ude0f'),
    (7, u'\ud83d\ude13'),
    (8, u'\ud83d\ude0d'),
    (9, u'\ud83d\ude2d'),
    (10, u'\ud83d\ude0e'),
    (11, u'\ud83d\ude44'),
    (12, u'\ud83d\ude05'),
    (13, u'\ud83d\ude02'),
    (14, u'\ud83d\udc4f'),
    (15, u'\ud83d\ude21'),
    (16, u'\ud83d\udc4d'),
    (17, u'\u2764\ufe0f'),
    (18, u'\u2600\ufe0f'),
    (19, u'\ud83c\udf39'),
    (20, u'\ud83d\udc4b'),
    (21, u'\ud83e\udd27'),
    (22, u'\ud83d\ude1f'),
    (23, u'\ud83e\udd29'),
    (24, u'\ud83d\ude12'),
    (25, u'\ud83e\udd2c'),
    (26, u'\ud83d\ude28'),
    (27, u'\ud83d\ude31'),
    (28, u'\ud83c\udf1b'),
    (29, u'\ud83d\udc36'),
    (30, u'\ud83d\ude09'),
    (31, u'\ud83d\udc31'),
    (32, u'\ud83e\udd2a'),
    (33, u'\ud83c\udf40'),
    (34, u'\u270c\ufe0f'),
    (35, u'\ud83c\udfc5'),
    (36, u'\u26bd\ufe0f'),
    (37, u'\ud83c\udfc6'),
    (38, u'\ud83c\udf89'),
    (39, u'\ud83c\udf7a'),
    (40, u'\ud83d\ude32'),
    (41, u'\ud83d\ude2b'),
    (42, u'\ud83d\ude35'),
    (43, u'\ud83e\udd14'),
    (44, u'\ud83d\ude09'),
    (45, u'\ud83d\udc47'),
    (46, u'\ud83e\udd11'),
    (47, u'\ud83d\ude33'),
    (48, u'\ud83e\udd2d'),
    (49, u'\ud83c\udf49'),
    (50, u'\ud83d\udc3c'),
    (51, u'\ud83d\udc94')
))


def encode_to_emoji(text):
    iterator = PATTERN.finditer(text)
    s = []
    offset = 0
    for m in iterator:
        j = m.start()
        s.append(text[offset: j])
        offset = m.end()
        # 替换逻辑
        s.append(_ID_EMOJI_MAP[int(m.groups()[0])])
    return u''.join(s) if s else text
