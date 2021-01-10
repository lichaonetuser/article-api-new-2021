# coding=utf-8
from logging.config import dictConfig
import yaml


def init_log_from_yaml(path):
    with open(path, 'r') as fp:
        config = yaml.load(fp)
    dictConfig(config)
