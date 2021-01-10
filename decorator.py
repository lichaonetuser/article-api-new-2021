# coding=utf8
import sys
import traceback
import json
from functools import wraps
from django.utils.cache import patch_cache_control
from django.http import HttpResponse

from pyutil.api.api_util import is_request_legal, verify_request_encryption


def request_validate(logger=None):
    '''
        验证 request 是否合法
    '''
    def decorator(func):
        @wraps(func)
        def func_wraper(request, **kargs):
            try:
                if is_request_legal(request):
                    return func(request, **kargs)
                if logger:
                    logger.info(
                        'func=%s request is illegal: udid=%s fmek=%s, fmev=%s',
                        func, request.GET.get('unique_device_id', ''),
                        request.GET.get('fmek'),
                        request.GET.get('fmev')
                        )
                return dict(
                    msg='request is illegal'
                    )
            except Exception as e:
                if logger:
                    et, ei, tb = sys.exc_info()
                    ftb = ''.join(traceback.format_tb(tb))
                    logger.info(
                        'func: %s, e=%s, %s error:%s, %s, %s',
                        func.__module__, e, et.__name__, ei.message, ftb
                        )
                return {}
        return func_wraper
    return decorator


def api_response(logger=None):
    def decorator(func):
        @wraps(func)
        def func_wraper(*args, **kargs):
            result = {}
            try:
                result["data"] = func(*args, **kargs)
                result["status"] = "1"
            except Exception as e:
                result["status"] = "2"
                result["info"] = "server error"
                result["error"] = str(e)
                if logger:
                    et, ei, tb = sys.exc_info()
                    ftb = ''.join(traceback.format_tb(tb))
                    logger.info(
                        'api %s error:%s, %s, %s',
                        func.__module__, et.__name__, ei.message, ftb
                        )
            return json.dumps(result)
        return func_wraper
    return decorator


def responsewrapper(func):
    def decarator(*args, **kargs):
        result = {}
        try:
            result["data"] = func(*args, **kargs)
            result["status"] = "1"
        except Exception as e:
            result["status"] = "2"
            result["info"] = "server error"
            result["error"] = str(e)
        return json.dumps(result)
    return decarator


def cachcontrol(**kwargs):
    def wrapper(func):
        def newfunc(request, *fargs, **fkwargs):
            result = func(request, *fargs, **fkwargs)
            patch_cache_control(result, **kwargs)
            return result
        return newfunc
    return wrapper


def request_prevent_dup(redis_pool=None, logger=None):
    '''
        防重复请求
    '''
    def decorator(func):
        @wraps(func)
        def _(request, **kwargs):
            try:
                rs, msg = verify_request_encryption(request, redis_pool)

                if rs:
                    return func(request, **kwargs)

                if logger:
                    logger.warning('func=%s request is illegal, error mesg=%s', func.__module__, msg)

                return HttpResponse(json.dumps({'status': '2', 'info': 'request is illegal'}))
            except Exception as e:
                if logger:
                    et, ei, tb = sys.exc_info()
                    ftb = ''.join(traceback.format_tb(tb))
                    logger.error(
                        'func: %s, e=%s, %s error:%s, %s, %s',
                        func.__module__, e, et.__name__, ei.message, ftb
                        )
                return HttpResponse(json.dumps({'status': '2', 'info': 'server error'}))

        return _

    return decorator
