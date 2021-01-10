# coding=utf-8
from jinja2 import Environment

from pyutil.api.api_util import parse_query_str
from pyutil.api.memcached_key import CACHE_STATIC_DATA_KEY, CACHE_STATIC_DATA_JSON_KEY
from pyutil.api.traffic import select_by_prob, select_by_hash, get_code_by_hash, select_by_udid, select_by_hash_ex,\
    select_by_ret_hash_ex, select_by_udid_gte_time, select_by_udid_group
from pyutil.api.ver import ver_gt, ver_gte, ver_lt, ver_lte, ver_eq
from pyutil.program.lru import LRUCache
from pyutil.text.conv import try_load_json


env = Environment()
env.globals['select_by_prob'] = select_by_prob
env.globals['select_by_hash'] = select_by_hash
env.globals['get_code_by_hash'] = get_code_by_hash
env.globals['select_by_udid'] = select_by_udid
env.globals['select_by_hash_ex'] = select_by_hash_ex
env.globals['select_by_ret_hash_ex'] = select_by_ret_hash_ex
env.globals['ver_gt'] = ver_gt
env.globals['ver_gte'] = ver_gte
env.globals['ver_lt'] = ver_lt
env.globals['ver_lte'] = ver_lte
env.globals['ver_eq'] = ver_eq
env.globals['select_by_udid_gte_time'] = select_by_udid_gte_time
env.globals['select_by_udid_group'] = select_by_udid_group


class StaticDataDAL(object):
    """
    可更新的静态数据访问.

    - 数据保存在的数据库user.static_data表中.
    - 数据的访问原则上总是从memcached中访问.
    - 数据的修改在运营端,修改后,要将指定的key删除掉.
    """
    def __init__(self, pool, cache=None, pool_name='user', cache_time=120, tpl_cache_size=0, env_dct={}):
        """
        :type pool: DBUtils.PooledDB.PooledDB
        :type cache: pyutil.program.cache.Cache
        :type pool_name: str
        :type cache_time: int
        :type tpl_cache_size: int
        :rtype: StaticDataDAL
        """
        self.db = pool.get(pool_name)
        self.cache = cache
        self.cache_time = cache_time
        if env_dct:
            env.globals.update(env_dct)

        # wrap methods
        if cache:
            self.get = self.cache.cache(pattern=CACHE_STATIC_DATA_KEY, expires=cache_time, is_bound=False)(self._do_get)
            self.get_json = self.cache.cache(
                pattern=CACHE_STATIC_DATA_JSON_KEY, expires=cache_time, is_bound=False)(self._do_get_json)
        else:
            self.get_json = self._do_get_json

        # memory cache
        self.memory_stores = {}
        self.should_tpl_cache = tpl_cache_size > 0
        if self.should_tpl_cache:
            self.tpl_cache = LRUCache(tpl_cache_size)

    def get(self, name):
        if name in self.memory_stores:
            return self.memory_stores[name]
        ret = self._get(name)
        if ret:
            self.memory_stores[name] = ret
        return ret

    def _get(self, name):
        conn = self.db.connection()
        cur = conn.cursor()
        ret = None
        try:
            cur.execute('select data from static_data where name = %s', (name, ))
            one = cur.fetchone()
            ret = one['data'] if one else None
        finally:
            cur.close()
            conn.close()

        return ret

    # @cache.cache(pattern=CACHE_STATIC_DATA_KEY, expires=CACHE_TIME, is_bound=True)
    def _do_get(self, name):
        return self._get(name)

    # XXX cache的失效由运营端控制
    # @cache.cache(pattern=CACHE_STATIC_DATA_JSON_KEY, expires=CACHE_TIME, is_bound=True)
    def _do_get_json(self, name, default=None):
        data = self._get(name)
        if default is None:
            default = {}
        ret = try_load_json(data, default)
        return ret

    def get_with_ctx(self, name, param_dict, use_tpl_cache=False):
        # use get() cache
        val = self.get(name)
        if not val:
            return val
        if isinstance(val, str):
            src = val.encode('utf-8').decode('utf-8')
        else:
            src = val.decode('utf-8')
        if use_tpl_cache and self.should_tpl_cache:
            src_hash = hash(src)
            if self.tpl_cache.contains(src_hash):
                tpl = self.tpl_cache.get(src_hash)
            else:
                tpl = env.from_string(src)
                self.tpl_cache.put(src_hash, tpl)
        else:
            tpl = env.from_string(src)
        return tpl.render(param_dict)

    def get_json_with_ctx(self, name, param_dict, use_tpl_cache=False):
        val = self.get_with_ctx(name, param_dict, use_tpl_cache=use_tpl_cache)
        val_json = try_load_json(val, {})
        return val_json

    def clear_memory_stores(self):
        self.memory_stores.clear()


def gen_ctx(request):
    """
    生成 static_data 带逻辑渲染的上下文对象
    :type request: django.http.HttpRequest
    :rtype: dict
    """
    query_str = parse_query_str(request)
    ctx = dict(query_str.__dict__)
    try:
        uid = request.session.get('uid', '')
        ctx['uid'] = uid
    except Exception as e:
        # api 没有安装 session 的情况
        pass
    return ctx
