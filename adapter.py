# coding=utf-8
import requests

import log
from api.advertise.dals import gen_ad_id
from pyutil.api.util import md5

LANDING_URL = 'http://www.x.com/share/advv?id={}&adv_id={}&url={}'

GCMOB_URL = 'http://sgrtb.mobgc.com/ssp/v1/get'
GCMOB_TOKEN_LARGE = '34308a1cb54c72a77b4137c6d0981f6b'
GCMOB_TOKEN_SMALL = 'f6f052a049e2490e3c5bffa8dc07515d'


logger = log.ad_logger


def gcmob(request, qs, token):
    m = {}
    m['ip'] = qs.ip
    m['os'] = 'ios' if qs.phone_type == 'iphone' else 'android'
    m['osv'] = qs.os_version
    m['adw'] = request.GET.get('adw', '768')
    m['adh'] = request.GET.get('adh', '1024')
    m['sw'] = m['adw']
    m['sh'] = m['adh']
    m['ppi'] = '326' if qs.device_type.lower().find('iphone') else '264'
    m['clickbrowser'] = 1
    m['ua'] = qs.user_agent
    m['connectiontype'] = '0'
    m['idfa'] = qs.idfa
    m['language'] = 'jp'
    m['token'] = token

    r = requests.get(GCMOB_URL, params=m)
    ret = r.json()
    logger.info('gcmob: {}, {}'.format(r.request.url, ret))

    # 生成广告结构
    if 'errormsg' in ret and ret['errormsg'] != 'ok':
        return {}

    items = []
    if 'image_ad' in ret:
        items.append({
        })
    elif 'html' in ret:
        landing = ret['html']
        ad_id = md5(landing)
        url = LANDING_URL.format(ad_id, gen_ad_id(), landing)
        items.append({
            "id": ad_id,
            "track": {
                "impression": [],
                "click": []
            },
            "type": 0,
            "web_url": url,
            "cover_image": "",
            "show_close_interval": 5,
            "auto_close_interval": 20
        })
    return items
