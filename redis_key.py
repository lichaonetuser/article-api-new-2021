# coding=utf8
from numpy import unicode

from api.user.types import User
from pyutil.text.conv import try_parse


def utf8(s):
    if isinstance(s, str):
        return s
    if isinstance(s, unicode):
        return s.encode('utf8')
    return s


def get_channel_all_groups_key(channel_id):
    return 'channel_%s_*' % (channel_id, )


def get_channel_groups_key(channel_id, index):
    return 'channel_%s_%s' % (channel_id, index)


def get_video_channel_groups_key(video_channel_id, index):
    return 'video_channel_%s_%s' % (video_channel_id, index)


def get_video_discover_group_playlists_key(index):
    return 'discover_playlist_%s' % (index)


def get_video_playlist_group_videos_key(playlist_id, index):
    return 'video_playlist_%s_%s' % (playlist_id, index)


def get_language_config_key(lang):
    return 'language_config_%s' % (lang, )


def get_language_config_fail_key():
    return 'language_config_fail'


def get_fake_users_key():
    return 'fake_users'


def get_old_rank_list_key():
    return 'old_rank_list'


def get_rank_list_key(app_name, lang, geo='jp'):
    if geo == 'ind' and lang == 'en':
        return 'rank_list_koreanfm_hindi'
    return 'rank_list_%s_%s' % (app_name, lang)


def get_language_rank_key(lang, rank_id):
    return 'lang_rank_%s_%s' % (lang, rank_id)


def get_rank_detail_key(rank_id, ):
    return 'rank_detail_%s' % rank_id


def get_lang_hotword_key(lang, ):
    return 'hotword_%s' % (lang, )


def get_new_lang_hotword_key(lang, ):
    return 'new_hotword_%s' % (lang, )


def get_top_artists_key(lang, ):
    return 'topartists_%s' % lang


def get_cdn_stats_key(sid, t='old'):
    return '%s-%s' % (t, sid)


def get_monitor_song_source_key(sid, title, artist, source_id, url):
    return "monitor_song_source_%s_%s_%d_%s" % (
        title, artist, source_id, url
        )


def get_monitor_song_source_queue_key():
    """使用这个key作为简单的mq，其value类型为list"""
    return "monitor_song_source_queue"


def get_user_prompt_key(device_id, active=1):
    if active:
        return 'active_user_prompt_%s' % device_id
    else:
        return 'unactive_user_prompt_%s' % device_id


def get_user_prompt_type_key(key):
    return 'common_user_prompt_%s' % (key, )


def get_prompt_key(appid, lang, ver):
    return "prompt_%s_%s_%s_key" % (appid, lang, ver)


def get_prompt_log_key(key, version, app_id, unique_device_id):
    return "%s_%s_%s_%s" % (key, version, app_id, unique_device_id)


def get_song_source_key(sid):
    return 'song_source_%s' % (sid, )


def get_source_proxy_key(source):
    return 'source_proxy_%s' % (source, )


def get_song_list_unique_device_id_key(unique_device_id):
    # 存储的redis key,进一步持久化存储到mongodb或mysql
    return 'song_list_%s' % (unique_device_id, )


def get_processing_song_list_key(unique_device_id):
    # 未完成的rebuild_song_list工作的unique_device_id
    return 'processing_%s' % (unique_device_id, )


def get_songlist_repair_key(title, artist):
    return 'songlist_repair_%s_%s' % (
        utf8(title.lower()), utf8(artist.lower()))


def get_songlist_unrepair_key():
    return 'songlist_unrepair_songs'


def get_music_artists_key(lang, ):
    return 'music_artist_%s' % (lang, )


def get_music_artist_detail_key(artist_id, lang):
    return 'music_artist_detail_%s_%s' % (artist_id, lang)


def get_blacklist_key(id):
    return "blacklist_%s" % (id)


def get_device_platform_key(unique_device_id):
    return 'device_platform_%s' % (unique_device_id)


def get_online_devices_key(uid):
    return 'online_devices_%s' % (uid)


def get_jspatch_key(app_id, v):
    return 'jspatch_%s_%s' % (app_id, v)


def get_songlist_server_key(uid):
    '''
        单个用户uid对应的所有服务端版本号
    '''
    return 'songlist_server_version_%s' % (uid, )


def get_songlist_list_key(uid):
    '''
        单个用户uid对应的歌单列表
    '''
    return 'songlist_list_%s' % (uid, )


def get_songlist_fav_list_key(uid):
    """
    用户收藏歌单列表
    """
    return "songlist_fav_list_%s" % uid


def get_songlist_detail_key(song_list_id):
    '''
        单个歌单song_list_id对应的歌曲数据
    '''
    return 'songlist_detail_%s' % (song_list_id, )


def get_songlist_detail_meta_key(song_list_id):
    """
        单个歌单song_list_id对应的歌单meta数据
    """
    return "song_list_detail_meta_%s" % song_list_id


def get_songlist_receive_version_key(id, id_type):
    '''
        记录客户端传输过来的client_send_version
    '''
    if id_type not in [User.TYPE_UID, User.TYPE_UNIQUE_DEVICE_ID]:
        raise Exception('id_type=%s not qualified' % id_type)
    return 'songlist_csv_%s_%s' % (id_type, id)


def get_songlist_receive_version_for_udid_key(unique_device_id):
    return 'songlist_csv_for_udid_%s' % unique_device_id


def get_songlist_fail_times_for_udid_key(unique_device_id):
    return 'songlist_cvs_fail_times_for_udid_%s' % unique_device_id


def get_songlist_play_count_key(songlist_id):
    return 'songlist_play_count_%s' % songlist_id


def get_songlist_re_sync_up_signal_for_udid_key(unique_device_id):
    return 'songlist_re_sync_up_signal_udid_%s' % (unique_device_id)


def get_songlist_resync_udids_key():
    '''
        记录当前需要重传的所有unique_device_id
        deprecated.
    '''
    return 'songlist_resync_udids'


def get_songlist_resync_uid_udid_key(uid, udid):
    return "songlist_resync_%s_%s" % (uid, udid)


def get_download_song_key(song_id):
    return 'download_song_id_%s' % (song_id, )


def get_camel_prompt_blacklist():
    return 'camel_prompt_blacklist'


def get_camel_prompt_counter():
    return 'camel_prompt_user_counter'


def get_camel_prompt_install():
    return 'camel_prompt_install_info'


def get_camel_prompt_num():
    return 'camel_prompt_num'


def get_search_artists_key():
    return 'search_artists'


def get_uid_info_key(uid):
    return 'uid_info_%s' % uid


def get_udid_info_key(udid):
    return 'udid_info_%s' % udid


def get_ftfb_info_key(ftfb):
    return 'ftfb_info_%s' % ftfb


def get_ftfb_uid_key(ftfb):
    return 'ftfb_info_%s' % ftfb


def get_ftfb_uid_v2_key(ftfb, app_type=0):
    if app_type == 0:
        return 'ftfb_info_%s' % ftfb
    else:
        return 'ftfb_info_%s_%s' % (ftfb, app_type)


def get_uid_account_key(uid):
    return 'account_%s' % uid


def get_platform_uid_key(platform, platform_uid):
    return '%s_%s_uid' % (platform, platform_uid)


def get_platform_uid_v2_key(platform, platform_uid, app_type=0):
    if app_type == 0:
        return '%s_%s_uid' % (platform, platform_uid)
    else:
        return '%s_%s_%s_uid' % (platform, platform_uid, app_type)


def get_in_review_app_key(app_id, version):
    return 'in_review_ip_%s_%s' % (app_id, version)


def get_in_review_key(app_id, version, ip):
    return 'in_review_%s_%s_%s' % (app_id, version, ip)


def get_youtube_artists_key(lang, ):
    return 'youtube_artists_%s' % (lang, )


def get_youtube_video_key(video_id):
    return 'youtube_video_%s' % (video_id, )


def get_youtube_channel_list_key(lang):
    return 'youtube_channel_list_%s' % lang


def get_youtube_channel_videos_key(channel_id, index):
    return 'youtube_channel_%s_%s' % (channel_id, index)


def get_youtube_discover_list_key(lang, ):
    return 'youtube_discover_list_%s' % (lang, )


def get_candidate_youtube_discover_list_key(lang):
    return 'candidate_youtube_discover_list_%s' % (lang, )


def get_youtube_playlist_detail_key(playlist_id, lang, page):
    return 'youtube_playlist_detail_%s_%s_%s' % (playlist_id, lang, page)


def get_youtube_hottest_videos_key(lang, page):
    return 'youtube_hottest_videos_%s_%s' % (lang, page)


def get_youtube_rank_detail_key(rank_id, lang, page):
    return 'youtube_rank_detail_%s_%s_%s' % (rank_id, lang, page)


def get_youtube_feedback_report_defect_key(video_id, ):
    return 'youtube_feedback_report_defect_%s' % (video_id, )


def get_youtube_query_log_key(lang):
    return 'youtube_query_log_%s' % (lang, )


def get_youtube_top_queries_key(lang):
    return 'youtube_top_queries_%s' % (lang, )


def get_service_monitor_key(entity_id, is_uid=True):
    return 'service_monitor_%s_%s' % ('uid' if is_uid else 'udid', entity_id)


def get_service_app_log_key(entity_id, is_uid=True):
    return 'service_app_log_%s_%s' % ('uid' if is_uid else 'udid', entity_id)


def get_song_key(id_):
    return str(id_)


def get_myfm_install_info_key(udid):
    return 'myfm_install_info_%s' % udid


def get_myfm_d_u_i_upload_key(udid, d_u_i_type):
    """d_u_i_type:
        "u_d": 当前唯一可用值
    """
    return "myfm_d_u_i_upload_%s_%s" % (udid, d_u_i_type)


def get_myfm_rank_song_list(rank_id):
    """
    热门歌单key
    :param rank_id:
    :return:
    """
    return 'myfm_rank_song_list_{}'.format(rank_id)


def get_myfm_rank_temp_song_list(rank_id):
    return 'myfm_rank_temp_song_list_{}'.format(rank_id)


def get_myfm_hottest_song_list(rank_id):
    return 'myfm_hottest_song_list_{}'.format(rank_id)


def get_myfm_rank_preset_key(type_id):
    """
    榜单按钮数据
    :param type_id:
    :return:
    """
    return 'myfm_rank_preset_{}'.format(type_id)


def get_doki_ad_counter(ad_id):
    return 'doki_ad_counter_%s' % (ad_id, )


def get_doki_ad_response_counter(ad_id, event):
    return 'doki_ad_response_%s_%s' % (ad_id, event)


def get_special_prompt_key():
    return 'special_prompt'


def get_special_prompt_user_count_key():
    return 'special_prompt_user_count'


def get_feedback_faq_key(lang, app_id=''):
    if not app_id:
        return 'feedback_faq_%s' % lang
    else:
        return 'feedback_faq_%s_%s' % (lang, app_id)


def get_musicbox_app_config_key():
    return 'musicbox_app_config'


def get_not_in_review_ip_key(ip):
    ip_3 = ('.').join(ip.split('.')[0:3])
    return 'not_in_review_ip_%s' % (ip_3, )


def get_not_in_review_ip_set_key():
    return 'not_in_review_ip_set'


def get_not_in_review_ip_hash_key():
    return 'not_in_review_ip_hash'


def get_cnc_song_key(sid):
    return 'cnc_%s' % (sid, )


def get_activity_top_hundred_key():
        return 'activity_top_hundred'


def get_activity_data_key():
    return 'activity_data'


def get_relation_counts_key(uid):
        return "relation_counts_%s" % uid


def get_relation_followings_key(uid):
    return "relation_followings_%s" % uid


def get_relation_followers_key(uid):
    return "relation_followers_%s" % uid


def get_relation_suggested_users_key(uid):
    return "relation_suggested_users_%s" % uid


def get_relation_op_suggested_users_key(uid):
    return "relation_op_suggested_users_%s" % uid


def get_feed_inbox_key(uid):
    """
    Feed 关注动态
    """
    return 'feed_inbox_{}'.format(uid)


def get_lyric_text_key(lyric_path):
    md5_path = lyric_path.split(".")[0]
    return "".join(md5_path.split("/"))


def get_song_id_md5_key(song_id_md5):
    return "song_id_md5_%s" % song_id_md5


def get_mv_song_id_key(song_id):
    return "mv_song_id_%s" % song_id


def get_user_message_count(uid):
    return 'user_message_count_%s' % uid


def get_user_notification_count(uid):
    return 'user_notification_count_%s' % uid


def get_device_notification_count(udid):
    return 'device_notification_count_%s' % udid


# 文章设备推送消息数量
def get_device_push_count(udid):
    return 'device_push_count_%s' % udid

# 文章device分组push记录存储key
def get_device_push_group_count(id_, udid):
    return 'device_push_group_count_%s_%s' % (id_, udid)


def get_device_all_notification_count(lang, udid):
        return 'device_all_notification_count_%s_%s' % (lang, udid)


def get_notification_group(id):
    return 'notification_group_%s' % id


def get_user_tag_ids_key(uid):
    return 'user_tag_ids_%s' % uid


def get_user_setting_key(uid):
    return 'user_setting_%s' % uid


def get_recommend_list_key(uid, date):
    '''
    generate redis key for user recommend songs
    uid: uid or udid
    '''
    return 'rec_user_predict_%s' % (uid,)


def get_recommend_list_key_default(date, lang='ja'):
    '''
    generate redis key for user recommend songs by default
    date: format, YYYYMMDD
    lang: 'ja' by default, 'zh-hant', 'en' optional
    '''
    return 'rec_default_predict_%s_%s' % (lang, date)


def get_recommend_dislike_list_key(uid, date):
    '''
    generate redis key for user dislike songs
    uid: uid or udid
    date: format, YYYYMMDD
    '''
    return 'rec_user_dislike_%s_%s' % (uid, date)


def get_recommend_channel_songs_key(id):
    '''
    generate redis key for user recommend songs of channel
    :param id: uid or udid
    :return:
    '''
    return 'rec_user_channel_songs_%s' % id


def get_youtube_url_key(yid):
    """
    生成 youtube 链接存储 key
    :type yid: str
    :rtype: str
    """
    return 'yid_{}'.format(yid)


def get_article_key(article_id):
    return 'article_%s' % (article_id)


def get_image_key(image_id):
    return 'image_%s' % (image_id)


def get_article_channel_list_key():
    return 'a_channel_list'


def get_article_channel_zset_key(channel_id, app_type=1):
    return 'a_channel_zset_%s_%s' % (app_type, channel_id)


def get_article_sub_category_zset_key(category_id, sub_category_id):
    return 'a_sub_category_%s_%s' % (category_id, sub_category_id)


def get_article_sub_category_channel_set_key(category_id, sub_category_id):
    return 'a_category_channel_%s_%s_set' % (category_id, sub_category_id)


def get_article_channel_sub_category_set_key(channel_id):
    return 'a_channel_category_%s_set' % (channel_id)


def get_update_article_offset_key(partition_id=0):
    return 'update_article_offset_%s' % (partition_id)


def get_article_reload_list_key():
    return 'a_reload_list'


def get_article_channel_category_rate_key(channel_id, category_id, sub_category_id):
    return 'a_channel_category_rate_%s_%s_%s' % (channel_id, category_id, sub_category_id)


def get_article_channel_category_bignews_rate_key(channel_id, category_id, sub_category_id):
    return 'a_channel_category_bignews_rate_%s_%s_%s' % (channel_id, category_id, sub_category_id)


def get_article_source_key(source_id):
    return 'a_source_key_%s' % (source_id)


def get_article_related_key(article_id):
    return 'a_related_%s' % (article_id, )


def get_related_item_key(related_type, item_id):
    return 'a_related_%s_%s' % (related_type, item_id)


def get_sport_ref_zset_key(item_type, sport_item_type, sport_item_id):
    return 'a_sport_ref_%s_%s_%s' % (item_type, sport_item_type, sport_item_id)


def get_sport_team_schedule_zset_key(team_id, season_id=0):
    return 'a_sport_team_schedule_%s_%s' % (season_id, team_id)


def get_update_sport_offset_key(topic_type='online', partition_id=0):
    return 'update_article_offset_%s_%s' % (topic_type, partition_id)


def get_breaking_news_zset_key(channel_id):
    return 'breaking_news_zset_%s' % (channel_id)


def get_breaking_news_hash_key(channel_id):
    return 'breaking_news_hash_%s' % (channel_id)


def get_article_app_log_key(partition_id=0):
    return 'article_app_log_key_{}'.format(partition_id)


def get_ad_hermes_creative_key(creative_id):
    return 'ad_creative_{}'.format(creative_id)


def get_ad_hermes_unit_key(ad_unit_name):
    return 'ad_unit_{}'.format(ad_unit_name)


def get_ad_query_words_key(ad_id):
    return 'ad_query_word_{}'.format(ad_id)


def get_world_cup_dig_count_hash_key():
    return 'world_cup_dig_count_hash'


def get_world_cup_dig_team_info_key():
    return 'world_cup_dig_team_info_key'


def get_world_cup_lottery_hash_key(match_id, team_id):
    # team_id = 0, draw
    return 'world_cup_lottery_%s_%s' % (match_id, team_id)


def get_doki_users_hset_key():
    return 'doki_user_hset'


def get_article_hot_zset_key():
    return 'article_hot_zset_key'


def get_songlist_self_recommend_key(song_list_id):
    return 'songlist_self_r_%s' % (song_list_id, )


def get_udid_idfa_key(unique_device_id, ):
    return 'idfa_%s' % (unique_device_id, )


# fm使用 article不适用
def get_udid_idfa_db(unique_device_id, ):
    if not unique_device_id:
        return 1
    remain = try_parse(unique_device_id.split('v')[0][-2:], int, 0)
    return remain / 10 + 1
