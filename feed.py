# coding=utf-8
from __future__ import absolute_import
import logging
from api.feed.models import Card


layout_321321 = (12, (3, 2, 1, 3, 2, 1))

logger = logging.getLogger('exc')


def mix_layout(items, master=layout_321321):
    """
    混合排版方法:
    其中`master`为母版格式, 为一个二元tuple A, 第一个元素是每屏元素数量, 第二个元素为一个tuple B, B的元素个数为行数,
    元素值为每行item数.
    :type items: list
    :type master: tuple
    :return: list
    """
    if len(items) != master[0]:
        logger.warning('size of items not matched the master size.items={},master={}'.format(items, master))
        return items
    ret = []
    i = 0
    for n in master[1]:
        ret.append(items[i:i + n])
        i += n
    return ret


def feed_mix_layout(items, master=layout_321321):
    """
    :type items: list[utils.api.APIModel]
    :param master:
    :return:
    """
    groups = mix_layout(items, master)
    ret = []
    for group in groups:
        if len(group) > 1:
            ret.append(Card(data=dict(items=group)))
        elif len(group) == 1:
            ret.append(group[0])
    return ret


def mix_adaptive_layout(items, predicate=lambda x: x.has_images()):
    """
    自适应排版:
        - 寻找连续子序列 [predicate为True]
        - 对每一个新发现的子序列
            - 按3, 2, 1分组
            - 最大适应

    :type items: list[utils.model.FeedItemMixin]
    :type predicate:
    :rtype: list[utils.models.FeedItemMixin]
    """
    ret = []
    subseq = []
    for item in items:
        if predicate(item):
            subseq.append(item)
        else:
            n = len(subseq)
            if n == 0:
                ret.append(item)
                continue

            i = 0
            while i < n:
                rest = n - i
                if rest >= 5:
                    ret.append(subseq[i:i + 2])
                    i += 2
                    ret.append(subseq[i:i + 2])
                    i += 2
                    ret.append(subseq[i])
                    i += 1
                    continue
                # if rest >= 3:
                #     ret.append(subseq[i:i + 3])
                #     i += 3
                #     continue
                elif rest >= 2:
                    ret.append(subseq[i:i + 2])
                    i += 2
                    continue
                elif rest == 1:
                    ret.append(subseq[i])
                    i += 1
                    continue
            ret.append(item)
            subseq = []

    n = len(subseq)
    if n > 0:
        i = 0
        while i < n:
            rest = n - i
            if rest >= 5:
                ret.append(subseq[i:i + 2])
                i += 2
                ret.append(subseq[i:i + 2])
                i += 2
                ret.append(subseq[i])
                i += 1
                continue
            # if rest >= 3:
            #     ret.append(subseq[i:i + 3])
            #     i += 3
            #     continue
            elif rest >= 2:
                ret.append(subseq[i:i + 2])
                i += 2
                continue
            elif rest == 1:
                ret.append(subseq[i])
                i += 1
                continue
    return ret


def feed_mix_adaptive_layout(items):
    ret = []
    rs = mix_adaptive_layout(items)
    for r in rs:
        if isinstance(r, list):
            ret.append(Card(data=dict(items=r)))
        else:
            ret.append(r)
    return ret
