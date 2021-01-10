# coding=utf-8
from api.settings import env_var, kafka_producer_pool, DEBUG
from pyutil.api.static_data import StaticDataDAL
from api.settings import redis_pool, mysql_pool, itag_table
from api.interest.dals import InterestDAL
from api.memcached_pool import static_data_cache, cache_lb_memcache_cli, memcache_cli
from redis import StrictRedis
from rq import Queue
from api.article.dals import ArticleDAL, BannerDAL
from api.search.dals import SearchDAL
from api.video.dals import VideoDAL, VideoHotlinkDAL
from api.comment.dals import CommentDAL
from api.adhoc.dals import VoteDAL, ExpSelectDAL, TemporalEmitDAL
from api.user_action.dals import UserActionDAL
from api.app_log.utils import AppLogEmitter
from api.feed.dals import GuideDAL
from api.sport.dals import SportDAL
from api.user.user_dal import UniqueDeviceInfoDAL
from api.utils.mark import MarkDAL
from api.favorite.dals import FavorDAL
from api.subscribe.dals import SubscribeDAL, UserBlockDAL
from api.channel.dals import ChannelDAL




if env_var in {'aws_online', 'aws_test'}:
    static_dal = StaticDataDAL(
        mysql_pool, pool_name='static_data', cache=static_data_cache, cache_time=0, tpl_cache_size=20)
else:
    static_dal = StaticDataDAL(mysql_pool, cache=static_data_cache, cache_time=0, tpl_cache_size=20)

api_job_queue = Queue('api', connection=StrictRedis(connection_pool=redis_pool['job_queue']))
ad_log_job_queue = Queue('ad_log', connection=StrictRedis(connection_pool=redis_pool['job_queue']))

interest_dal = InterestDAL(redis_pool['article_channel'])
subscribe_dal = SubscribeDAL(mysql_pool['article_api'], redis_pool, itag_table, cache_lb_memcache_cli, static_dal)
article_dal = ArticleDAL(
    mysql_pool['article_api'], redis_pool['article_detail'], redis_pool['article_related'], memcache_cli)
search_dal = SearchDAL()
comment_dal = CommentDAL(api_job_queue)
video_dal = VideoDAL(redis_pool['youtube_hotlink'])
video_queue_dal = VideoHotlinkDAL(redis_pool['youtube_hotlink_queue'])
temporal_emit_dal = TemporalEmitDAL(redis_pool['guide'])
user_action_dal = UserActionDAL(redis_pool, api_job_queue, subscribe_dal)

app_log_emitter = AppLogEmitter(kafka_producer_pool['pb_app_log'], topic='article_pb_app_log')
monitor_emitter = AppLogEmitter(kafka_producer_pool['pb_app_log'], topic='article_pb_monitor')
guide_dal = GuideDAL(redis_pool['guide'])
exp_select_dal = ExpSelectDAL(redis_pool['guide'])
sport_dal = SportDAL(mysql_pool['article_api'])

banner_dal = BannerDAL(redis_pool['article_banner'], static_dal, sport_dal)
udinfo_dal = UniqueDeviceInfoDAL(redis_pool['udid_status'])

generic_mark_dal = MarkDAL('mark_st_{}_{}', redis_pool['guide'])
vote_dal = VoteDAL()
favor_dal = FavorDAL()
user_block_dal = UserBlockDAL()
channel_dal = ChannelDAL(conn_pool=redis_pool['article_channel'], static_dal=static_dal, DEBUG=DEBUG)

