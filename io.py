# coding=utf-8
import yaml


def load_yaml(path, use_include=False, include_tag='++include'):
    """
    :type path: str
    :type use_include: bool
    :type include_tag: str
    :rtype: dict
    """
    with open(path, 'r') as fp:
        ret = yaml.load(fp)
    if use_include and include_tag in ret and include_tag is not None and include_tag.strip() != '':
        with open(ret[include_tag], 'r', encoding='utf8') as fp:
            c = yaml.load(fp)
            ret.update(c)
            del ret[include_tag]
    return ret


def read_file(path):
    with open(path, 'r', encoding='utf8') as fp:
        return fp.read()
