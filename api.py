import json
from functools import wraps
import logging
import os
from django.http import JsonResponse
from api.utils.constants import IMAGE_TYPE
from future.utils import iteritems
from api.constants import EnumUserIdType
from pyutil.text.conv import try_load_json
import requests
from django.http import JsonResponse, HttpResponse

exc_logger = logging.getLogger('exc')

class APIModel(object):
    def __init__(self):
        self.id = 0
        self.item_id = 0
        self.aid = ''

    def init(self, data):
        """
        辅助方法, 用于把接受到的数据写入指定的属性
        :type data: dict
        """
        if not data:
            return
        for k, v in iteritems(data):
            if k in self.__dict__:
                self.__dict__[k] = v

    @classmethod
    def from_json(cls, json_str):
        """
        从 json 字符串中生成对象
        :type json_str: str
        :return:
        """
        data = try_load_json(json_str, {})
        if not data:
            return None
        obj = cls()
        obj.init(data)
        return obj

    def as_dict(self):
        """
        用于生成 dict 输出到服务端, 子类可以 override 该方法, 实现自定义逻辑
        :rtype: dict
        """
        return self.__dict__

    def normalize(self, ctx):
        return self

    def __repr__(self):
        return self.__class__.__name__ + json.dumps(self.as_dict())



class APIModelJSONEncoder(json.JSONEncoder):
    """
    API model JSON encoder
    """
    def default(self, o):
        try:
            obj = o.as_dict() if o is not None else o
            return obj
        except Exception as e:
            exc_logger.exception('APIModelJSON_error:o={}'.format(o))
            raise e


def json_api(*args, **kwargs):
    """
    JSON-API 统一接口格式

    kwargs:
        - exc_logger 异常日志名称
    :type exc_logger: str
    """
    def _0(f):
        @wraps(f)
        def _1(*args, **kwargs):
            ret = {'status': 1}
            internal_error = False
            ret['data'] = f(*args, **kwargs)
            status = 500 if internal_error else 200
            return JsonResponse(ret, encoder=APIModelJSONEncoder, status=status)
        return _1
    return _0


def get_jason_from_server(request, targeturl):
    method = request.method
    params = request.GET
    query = ''
    if params:
        query += '?'
        for key, value in params.items():
            query += str(key) + '=' + str(value) + '&'
        query = query[:-1]

    targeturl = targeturl + query
    params = {}

    if method == 'GET':
        response = requests.get(url=targeturl, params=params)
    else:
        postBody = request.body
        response = requests.post(url=targeturl, data=postBody)

    return HttpResponse(response.text)


def get_pk(request):
    """
    获取用户主键, 如果有 uid, 使用 uid; 如果没有, 使用 unique_device_id
    :type request: django.http.HttpRequest
    :rtype: (str, pyutil.api.api_util.QueryStr)
    """
    # return request.GET.get('unique_device_id'), None
    # FIXME
    from pyutil.api.api_util import parse_query_str
    from pyutil.text.conv import is_blank

    uid = request.session.get('uid', '')
    query_str = parse_query_str(request)
    if is_blank(uid):
        uid = query_str.unique_device_id
    return uid, query_str


def is_review_mode(query_str):
    """
    :type query_str: pyutil.api.api_util.QueryStr
    :rtype: bool
    """
    # if query_str.app_id == AppIds.Article_NewsTime and query_str.version.startswith('1.0'):
    # return False
    # if query_str.phone_type == 'iphone' and query_str.version.startswith('7.7.10'):
    #      return True
    return False

def get_image_type(img_name):
    _, ext = os.path.splitext(img_name.lower())
    return IMAGE_TYPE.get(ext)


def delete_item_fields(item, fields):
    for field in fields:
        if hasattr(item, field):
            delattr(item, field)

def get_pk_utype(uid, udid):
    return (uid, EnumUserIdType.UID) if uid else (udid, EnumUserIdType.UDID)
