# coding=utf-8
"""
    所有与memcached cache相关的key,都是用python string format.
    key要尽可能短,使用`.`来划分namespace.

    https://docs.python.org/2/library/string.html#format-string-syntax
"""


# all tags
CACHE_TAGS = 'c.t.all'

# static data of key
CACHE_STATIC_DATA_KEY = 'c.sd.{}'

# static json data of key
CACHE_STATIC_DATA_JSON_KEY = 'c.sd.j.{}'

# keys of static data module
CACHE_STATIC_DATA_KEYS = (CACHE_STATIC_DATA_KEY, CACHE_STATIC_DATA_JSON_KEY)

# ab test key
CACHE_AB_TEST_KEY = 'ab.test.{}.{}'
CACHE_AB_TEST_V2_KEY = 'ab.test.{}'

# ab test store key
CACHE_AB_TEST_STORE_KEY = 'ab.test.store'

# ab test whitelist key
CACHE_AB_TEST_WHITE_LIST_KEY = 'ab.whitelist'

# ab test app name map key
CACHE_AB_TEST_APP_NAME_MAP_KEY = 'ab.app.name.map.key'

# fav song lists by uid
CACHE_FAV_FAV_LIST_KEY = 'c.f.l.{}.{}'

# fav users by song_list_id
CACHE_FAV_FAV_USERS_KEY = 'c.f.u.{}'

# whether a uid user favorated a song_list_id list
CACHE_FAV_HAS_FAV_KEY = 'c.f.hf.{}'

# fav count
CACHE_FAV_COUNT_KEY = 'c.f.n.{}'

# share count
CACHE_SHARE_COUNT_KEY = 'c.sh.n.{}'

# song list other detail, by (song_list_id, lang)
CACHE_SONG_LIST_OTHER_DETAIL_KEY = 'c.sl.d.{}.{}'

# rank song list
CACHE_RANK_SONG_LIST_KEY = 'c.r.s.l.{}.{}.{}'

# activity rank list
CACHE_ACTIVITY_RANK_LIST_KEY = 'c.a.r.l'

# user moment
CACHE_USER_MOMENT_KEY = 'c.u.m.{}.{}'

# hot comments
CACHE_HOT_COMMENTS = 'c.c.h.c.{}.{}'

# comments load
CACHE_LOAD_COMMENTS = 'c.c.l.{}.{}.{last_id}.{limit}'

# song infomation
CACHE_SONG_INFOMATION = 'c.s.i.{}'

# comment count, target_type, target_id
CACHE_COMMENT_COUNT = 'c.c.c.{}.{}'

# comment by id
CACHE_COMMENT_BY_ID = 'c.c.id.{}'

# mvhub_discover_list
CACHE_MVHUB_DISCOVER_LIST_KEY = 'c.m.d.l.{}.{}'

# default_recommend_list
CACHE_DEFAULT_RECOMMEND_LIST = 'c.d.r.l.{}'

# user_upload_history
CACHE_USER_UPLOAD_HISTORY_KEY = 'c.u.u.h.{uid}.{limit}.{offset}'

# user_favor_articles
CACHE_USER_FAVOR_ARTICLES_KEY = 'c.u.f.a.{}'

# search_term_result
CACHE_SEARCH_TERM_RESULT_KEY = 'c.s.t.r.{}'

# search_term_result 区分分类(文章、视频)
CACHE_TYPE_SEARCH_TERM_RESULT_KEY = 'c.t.s.t.r.{}.{}'

# user_search_term_bool
CACHE_USER_SEARCH_TERM_BOOL_KEY = 'c.u.s.t.b.{}.{}'

# user_search_term_bool, 区分文章/视频
CACHE_USER_TYPE_SEARCH_TERM_BOOL_KEY = 'c.u.t.s.t.b.{}.{}.{}'

# aritcle hot words
CACHE_ARTICLE_HOT_WORDS_KEY = 'c.a.h.w.{}'

# aritcle hot words, 区分文章/视频
CACHE_TYPE_ARTICLE_HOT_WORDS_KEY = 'c.t.a.h.w.{}.{}'

# article user select info
CACHE_ARTICLE_USER_SELECT_INFO_KEY = 'c.a.u.s.i.{}'

# sport season player stats
CACHE_SPORT_SEASON_PLAYER_STATS_KEY = 'c.s.s.p.s.{}'

# sport season team stats
CACHE_SPORT_SEASON_TEAM_STATS_KEY = 'c.s.s.t.s.{}'

# sport season schedule api key
CACHE_SPORT_SEASON_SCHEDULE_API_RANK_KEY = 'c.s.s.s.a.r.{}'

# sport season team players
CACHE_SPORT_SEASON_TEAM_PLAYERS_KEY = 'c.s.s.t.p.{}.{}'

# sport season player
CACHE_SPORT_SEASON_PLAYER_KEY = 'c.s.s.p.{}.{}'

# sport team key
CACHE_SPORT_TEAM_KEY = 'c.s.t.{}'

# sport match key
CACHE_SPORT_MATCH_KEY = 'c.s.m.{}'

# sport match day schedule key
CACHE_SPORT_MATCH_DAY_KEY = 'c.s.m.d.{}'

# sport season schedule advance key
CACHE_SPORT_SEASON_SCHEDULE_ADVANCE_KEY = 'c.s.s.s.a.{}'

# user subscribe sources key
CACHE_USER_SUBSCRIBE_SOURCES_KEY = 'c.u.s.s.{}'

# source group key
CACHE_SOURCE_GROUP_KEY = 'c.s.g.{}'

# 24小时热闻卡片aids key
CACHE_TOP_HOT_ARTICLES_KEY = 'c.t.h.a'
