# coding=utf-8
import hashids

# 文章类型
from api.utils.lru import LRUSetCache

DATA_TYPE_ARTICLE = 1
# 分类类型
DATA_TYPE_CATEGORY = 2
# 频道分类lru.py
DATA_TYPE_CHANNEL = 3
# 体育分类
DATA_TYPE_SPORT = 4
# source group分类, 与DATA_TYPE_ARTICLE取值相同
DATA_TYPE_SOURCE_GROUP = DATA_TYPE_ARTICLE
# 兴趣标签
DATA_TYPE_ITAG = 5


def _h(salt):
    return hashids.Hashids(salt)


# salt 生成方式:
#   base64(read('/dev/urandom', 10))
_id_hashes = {
    DATA_TYPE_ARTICLE: _h('D6QvCfxdSCMjaA'),
    DATA_TYPE_CATEGORY: _h('oX+DARpVu1nRUA'),
    DATA_TYPE_CHANNEL: _h('tcXKhv++/cAjXg'),
    DATA_TYPE_SPORT: _h('o5LikpdZregFet'),
    DATA_TYPE_ITAG: _h('t73jdfheqtevj+i'),
}

encrypted_type_id_cache = {
    DATA_TYPE_ARTICLE: LRUSetCache(100000),
    DATA_TYPE_CATEGORY: LRUSetCache(10000),
    DATA_TYPE_CHANNEL: LRUSetCache(10000),
    DATA_TYPE_SPORT: LRUSetCache(10000),
    DATA_TYPE_ITAG: LRUSetCache(10000),
}


def encrypt_id(data_type, id_):
    """
    :type data_type: int
    :type id_: int
    :rtype: str
    """
    # return _id_hashes[data_type].encode(id_)
    if data_type not in encrypted_type_id_cache:
        return _id_hashes[data_type].encode(id_)

    lru_cache = encrypted_type_id_cache[data_type]
    encrypted_id = lru_cache.get(id_, None)
    if encrypted_id is None:
        encrypted_id = _id_hashes[data_type].encode(id_)
        lru_cache.put(id_, encrypted_id)
    return encrypted_id


def decrypt_id(data_type, s):
    """
    :type data_type: int
    :type s: str
    :rtype: int
    """
    r = _id_hashes[data_type].decode(s)
    if not r:
        raise ValueError('Illegal hashids value to decode')
    return r[0]
