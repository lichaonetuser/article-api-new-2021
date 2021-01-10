# coding=utf-8
import json

from django.views.decorators.csrf import csrf_exempt

from api.env import video_dal, video_queue_dal
from api.log import api_logger
from pyutil.text.conv import is_blank
from api.utils.api import json_api
import requests
from django.http import JsonResponse, HttpResponse



#@json_api()
def url(request):

    '''

        临时修改2021-1

    yid = request.GET.get('y_video_id', '')
    if is_blank(yid):
        return {}
    urls = video_dal.urls((yid, ))
    if not urls:
        video_queue_dal.queue_jump(yid)
        api_logger.info('video_url_jump_queue:{}'.format(yid))
    return urls.values()[0] if urls else {}
    '''
    url = request.path[1:].split('/')
    url = url[0] + '//' + url[1] + '/'
    url = request.path[1:].replace(':/', '://')  # 获得目标url
    host = request.get_host()
    method = request.method
    params = request.GET
    query = ''
    if params:
        query += '?'
        for key, value in params.items():
            query += str(key) + '=' + str(value) + '&'
        query = query[:-1]

    # http://152.32.147.133:8080/youtube/video/url/

    params = {}
    url = 'http://192.168.20.230:8080/youtube/video/url/' + query

    if method == 'GET':
        response = requests.get(url=url, params=params)
    else:
        postBody = request.body
        response = requests.post(url=url, data=postBody)

    return HttpResponse(response.text)

@json_api()
@csrf_exempt
def url_report(request):
    p = json.loads(request.body)
    if not p or 'url' not in p or 'y_video_id' not in p:
        return {}
    video_dal.report(p['y_video_id'], p['url'])
    return {}
