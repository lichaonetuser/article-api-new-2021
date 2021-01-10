# coding=utf-8
"""
AB test helpers
"""
import logging

from pyutil.text.conv import is_blank


# 层分割符
LAYER_SEP = '#'
# 实验分割符
EXP_SEP = '|'


class ABEval(object):
    """
    在一个请求有多个实验的场景下使用
    """
    def __init__(self):
        # <layer_id, {experiments, ...}>
        self.experiments = {}
        self.pk = ''

    @staticmethod
    def eval(e_flag, pk):
        if is_blank(e_flag):
            return ABEval()
        experiments = e_flag.split(EXP_SEP)
        r = ABEval()
        r.pk = pk
        for exp in experiments:
            try:
                layer_id, exp_name = exp.split(LAYER_SEP)
                if layer_id in r.experiments:
                    r.experiments[layer_id].add(exp_name)
                else:
                    r.experiments[layer_id] = {exp_name, }
            except:
                logging.getLogger('exc').exception('ABEval.eval()_error: e_flag={},pk={}'.format(e_flag, pk))
        return r

    def by_layer(self, layer_id):
        return self.experiments.get(layer_id, set([]))

    def is_in(self, layer_id, exp_name):
        return (layer_id in self.experiments) and (exp_name in self.experiments[layer_id])

    def __repr__(self):
        return 'ABEval<pk={},experiment={}>'.format(self.pk, self.experiments)


def ab_test_first(e_flag, layer_id, exp_name):
    """
    一次性检查逻辑, 在一个请求只有一个实验的场景下使用
    :param e_flag:
    :param layer_id:
    :param exp_name:
    :return:
    """
    if is_blank(e_flag):
        return False
    experiments = e_flag.split(EXP_SEP)
    for exp in experiments:
        try:
            layer_id, exp_name = exp.split(LAYER_SEP)
            if layer_id == layer_id and exp_name == exp_name:
                return True
        except:
            logging.getLogger('exc').exception('ab_test_first()_error: e_flag={}'.format(e_flag))
    return False


# ---------- AB 实验配置表,值的来源是配置表,此处主要是簿记 ----------
# 推荐实验层
AB_LAYER_RECSYS = '5'
# TAG实验层
AB_LAYER_TAG = '6'
# 功能卡片实验层
AB_LAYER_CARD = '7'
# serv 分流量实验层
AB_LAYER_SERV = '8'

# 标签是否显示实验
AB_EXPT_TAG = 'tag01'
# 动画卡片实验
AB_EXPT_CARD_PUSH = 'push_animate'
