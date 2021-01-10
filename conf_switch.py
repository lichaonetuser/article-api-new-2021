# coding=utf-8
import os


# 环境变量key
ENV_KEY = 'PUSIC_ENV'


def switch(path, env_key=ENV_KEY):
    if path is None or path.strip() == '':
        raise Exception('Path is blank.')
    var = os.environ.get(env_key, None)
    if var is None:
        return path
    # default value is prod
    part_path, ext = os.path.splitext(path)
    return part_path + '.' + var + ext


def get_env(env_key=ENV_KEY):
    var = os.environ.get(env_key, None)
    return var
