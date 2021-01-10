# coding=utf-8
from __future__ import absolute_import
import time
import random

from api.article.models import Article
from api.constants import EnumItemType, EnumCoverSize
from api.feed.models import Card
from api.utils.tag import TAGS
from api.video.models import Video
from api.sns_item.models import TwitterImage, GIF


def mock_single_image():
    i = random.randint(0, 100)
    v = TwitterImage(dict(
        id=i,
        title=u"{} 「みんなプレゼントもろたか〜？おれはちゅ〜るもろたで、きのう」＠婿".format(i),
        aid='SITEST{}'.format(i),
        source_id=1,
        source_name=u'ふーちゃん＠ねこ休み展',  # screen_name
        # channel_name = u'Twitter',
        source_pic='https://pbs.twimg.com/profile_images/813043776180535296/vJRI39dt_normal.jpg',
        # cover_image="https://pbs.twimg.com/media/DR2FtD7U8AAcadK.jpg",
        # twitter_id ="945058550505644032",
        avatar_url='https://pbs.twimg.com/profile_images/813043776180535296/vJRI39dt_normal.jpg',
        original_site_url='https://twitter.com/foochan0711',
        image={
            'type': 1,
            'width': 480,
            'height': 320,
            'urls': ['https://pbs.twimg.com/media/DR2FtD7U8AAcadK.jpg', ],
        },
        published_at=1514274372625,
        emit_time=int(time.time() * 1000),
    ))
    return v


def mock_video():
    i = random.randint(0, 100)
    v = Video(dict(
        id=i,
        title="{} ゆず「友　〜旅立ちの時〜」".format(i),
        description="ゆず38th Single「友　〜旅立ちの時〜」 配信：iTunes Store、レコチョクにて好評配信中 期間限定盤：2013年9月18日（水）"
                    "リリース http://amzn.to/12OSMld 「友　〜旅立ちの時〜」は「第80回NHK全国学校音楽コンクール」（Nコン）中学校の部"
                    " 課題曲、そして8〜9月度のNHK総合 / Eテレ「みんなのうた」に起用されたミディアムバラード。 Music Videoは、レコーデ"
                    "]ィングの模様をドキュメンタリー風に切り取った映像に仕上がりました。このMVは期間限定盤付属DVDに収められます。 "
                    "ゆずオフィシャルサイト：http://www.senha-yuzu.jp/ ゆず｜TOY'S FACTORY：http://www.toysfactory.co.jp/artist/yuzu",
        cover_image="https://i.ytimg.com/vi/WgAhMfhdZ4c/mqdefault.jpg",
        y_video_id="WgAhMfhdZ4c",
        emit_time=int(time.time() * 1000),
        duration_interval=90
    ))
    return v


def mock_article():
    a = Article({
        "detail_image_urls": [
            "https://cdn.getnewseveryday.com/ori_image/a3/1a1745dcfb35018d85047aae6d0dd5.jpg",
            "https://cdn.getnewseveryday.com/ori_image/81/69cae8225e5ea6197d7c43c23df59a.jpg",
            "https://cdn.getnewseveryday.com/ori_image/88/04c9aee8796a33319dd7b38ea2ae20.jpg"
        ],
        "source_name": "Engadget 日本版",
        "comment_type": 1,
        "related": [],
        "source_id": 29495,
        "published_at": 1502684640000,
        "is_favorite": False,
        "dig_count": 0,
        "is_digged": False,
        "source_pic": "https://cdn.getnewseveryday.com/icons/article/source/29495.jpg",
        "style": 3,
        "list_image_urls": [
            "https://cdn.getnewseveryday.com/image/a3/1a1745dcfb35018d85047aae6d0dd5.jpg",
            "https://cdn.getnewseveryday.com/image/81/69cae8225e5ea6197d7c43c23df59a.jpg",
            "https://cdn.getnewseveryday.com/image/88/04c9aee8796a33319dd7b38ea2ae20.jpg"
        ],
        "bury_count": 0,
        "title": "ポケモンGOでミュウツーが新システムで一般解禁「招待状」が必須",
        "url": "http://news.livedoor.com/article/detail/13473299/",
        "cr_type": 0,
        "share_url": "http://test.api.x.com/webnews/news_share?aid=PybGQ",
        "content": "\n<div class=\"main\">\n<div id=\"news_top\">\n  <h1 class=\"news_title\">ポケモンGOでミュウツーが新システムで一般解禁「招待状」が必須</h1>\n  <div class=\"news_source\">\n    <div class=\"source_pic\">\n      <img src=\"icons/article/source/29495.jpg\" width=\"204\" height=\"34\"/>\n    </div>\n    <div class=\"source_name\"></div>\n    <div class=\"source_time\">\n      <span class=\"news_date\">2017-08-14</span>\n      <span class=\"news_time\">13:24:00</span>\n    </div>\n  </div>\n</div>\n<div id=\"news_body\"><img src=\"ori_image/a3/1a1745dcfb35018d85047aae6d0dd5.jpg\" id=\"127545\" width=\"640\" height=\"336\"><p>横浜の『ポケモンGOスタジアム』イベントで先行出現した伝説のポケモン『ミュウツー』は、新システム『EXレイド』で一般解禁されることが分かりました。</p><p>【ギャラリー】横浜ポケモンGOスタジアムでミュウツー出現 (9枚)</p><img src=\"ori_image/81/69cae8225e5ea6197d7c43c23df59a.jpg\" id=\"127546\" width=\"409\" height=\"700\"><p>これまで解禁された伝説のポケモン(ルギア、フリーザー、ファイヤー、サンダー)は、いずれも高難度ながら通常と同じ流れのレイドバトルで捕獲できました。</p><p>しかしミュウツーからは、新システム『EXレイド』を通じた特別なレイドバトルでのみ挑戦できるようになります。</p><p>新システム『EXレイド』は、</p><p>・特定のジムで発生。参加には『招待状』が必要。</p><p>・招待状は、EXレイドが発生するジムで、過去の近い時期にレイドバトルに勝利したトレーナーが受け取れる(チャンスがある)。</p><p>・招待状はEXレイド開始時刻が記されている。</p><p>・招待状はEXレイド開始までかなり余裕をもって入手できるため、他のトレーナーと協力して事前に計画が可能。</p><p>つまりEXバトルの場合、たまたま近くを通りかかったり、始まってから駆けつけても、招待状がない場合は挑戦できません。</p><p>挑戦状を手に入れるには、EXレイドが実施されるジムで、近い時期にレイドに勝利しておくことが必要です。(どの程度の期間なのかは現時点で不明)。</p><p>要はできるだけ多くの場所で、できるだけ頻繁にレイドバトルに勝利しておくことが、招待状ゲットとEXレイド参加の確率を高めることになります。</p><p>(旅行先でたまたまレイド参戦したジムから招待状が届いたりしたら悩むことになりそうです)。</p><p>EXレイドは、今後数週間のうちにも実施される予定。ミュウツー以外のポケモンも、このEXレイドに登場します。</p><p>これまでの伝説のポケモンは、イベントで配布が発表された『詫びルギア』をはじめ、直後に一般解禁されて誰でもゲットの可能性がありました(レイドに勝てる人数が集まる地域なら)。</p><p>しかしミュウツーは、今後少なくとも数週間は、本日横浜スタジアムのイベントで手に入れたトレーナーしか持っていないプレミアム感のある伝説のポケモンになります。</p><p>速報：横浜でミュウツーをゲット！ポケモンGOスタジアム限定、一般解禁はどうなる？ </p><img src=\"ori_image/88/04c9aee8796a33319dd7b38ea2ae20.jpg\" id=\"127547\" width=\"4800\" height=\"2520\"><p>EXレイドの発表とあわせて、現在までに一般解禁済みの伝説のポケモンであるルギア、フリーザー、ファイヤー、サンダーのアンコール出現スケジュールも明らかになりました。</p><p>従来発表では、8月15日までサンダー出現、ルギアは「今後しばらく出現」の予定でした。</p><p>新発表によると、この4種は8月15日から9月1日まで継続して出現するとのこと。三鳥を逃して涙を飲んだ皆さんにはリベンジの機会です。</p><p>【ギャラリー】横浜ポケモンGOスタジアムでミュウツー出現 (9枚)</p></div>\n</div>",
        "emit_time": 0,
        "copyright_source_id": 0,
        "type": 0,
        "is_buried": False
    })
    return a


def mock_card(query_str):
    card = Card({
        'items': [
            mock_video().normalize(query_str),
            mock_article(),
        ],
        'emit_time': int(time.time() * 1000),
        'aid': '1'
    })
    return card


def mock_gif_image():
    return {
        'urls': ['https://lumiere-a.akamaihd.net/v1/images/findingnemo-_hi_bye_yes_02b6b2e9.gif'],
        'height': 180,
        'width': 320,
    }


def mock_mp4_video():
    return {
        'urls': ['https://video.twimg.com/tweet_video/DNCI3sUUQAAt6LH.mp4'],
        'width': 500,
        'height': 270,
        'duration': 16,
    }


def mock_gif():
    gif_type = random.randint(1, 2)
    r = GIF(data={
        'id': random.randint(0, 100),
        'image': mock_gif_image(),
        'video': mock_mp4_video(),
        'screen_name': 'sakamobi',
        'avatar_url': 'https://pbs.twimg.com/profile_images/818108384956162048/KDcNTk0w_normal.jpg',
        'homepage_url': 'https://twitter.com/sakamobi',
        'content': '理科ってやっぱり面白い！身近なアイテムで光の屈折を体験しよう',
        'gif_type': gif_type,
        'cover_image': 'https://pbs.twimg.com/tweet_video_thumb/DNCI3sUUQAAt6LH.jpg',  # if gif_type == 1 else 'https://lumiere-a.akamaihd.net/v1/images/findingnemo-_hi_bye_yes_02b6b2e9.gif'
    })
    return r


def mock_multiple_image():
    i = random.randint(0, 100)
    v = TwitterImage(dict(
        id=i,
        item_id=i,
        title=u"{} 「みんなプレゼントもろたか〜？おれはちゅ〜るもろたで、きのう」＠婿".format(i),
        aid='SITEST{}'.format(i),
        type=EnumItemType.MULTIPLE_IMAGE,
        source_id=1,
        source_name=u'ふーちゃん＠ねこ休み展',  # screen_name
        # channel_name = u'Twitter',
        source_pic='https://pbs.twimg.com/profile_images/813043776180535296/vJRI39dt_normal.jpg',
        # cover_image="https://pbs.twimg.com/media/DR2FtD7U8AAcadK.jpg",
        # twitter_id ="945058550505644032",
        avatar_url='https://pbs.twimg.com/profile_images/813043776180535296/vJRI39dt_normal.jpg',
        original_site_url='https://twitter.com/foochan0711',
        images=[
            {
                'type': 1,
                'width': 480,
                'height': 320,
                'urls': ['https://pbs.twimg.com/media/DR2FtD7U8AAcadK.jpg', ],
            },
            {
                'type': 1,
                'width': 480,
                'height': 320,
                'urls': ['https://pbs.twimg.com/media/DV0z_q6VoAAQtuY.jpg', ],
            },
            {
                'type': 1,
                'width': 480,
                'height': 320,
                'urls': ['https://pbs.twimg.com/media/DVoJRytVMAAb8OJ.jpg', ],
            },
        ],
        published_at=1514274372625,
        emit_time=int(time.time() * 1000),
    ))
    random.shuffle(v.images)
    return v


def mock_article_embed_video():
    html = '''
<div class="main">
    <div id="news_top">
        <h1 class="news_title">ポケモンGOでミュウツーが新システムで一般解禁「招待状」が必須</h1>
        <div class="news_source">
            <div class="source_pic">
                <img src="icons/article/source/29495.jpg" width="204" height="34"/>
            </div>
            <div class="source_name"></div>
            <div class="source_time">
                <span class="news_date">2017-08-14</span>
                <span class="news_time">13:24:00</span>
            </div>
        </div>
    </div>
    <div id="news_body"><img src="ori_image/a3/1a1745dcfb35018d85047aae6d0dd5.jpg" id="127545" width="640" height="336">
        <div class="video_box" style="height: 180px;">
            <video src="https://video.twimg.com/ext_tw_video/969249655220588544/pu/vid/256x320/OKIAxZ-iHT1Mj-MB.mp4"
             poster="https://pbs.twimg.com/ext_tw_video_thumb/969249655220588544/pu/img/jt6tf8gj9HkEn2E_.jpg"></video>
            <span>2:30</span>
            <i></i>
        </div>
        <p>・招待状はEXレイド開始までかなり余裕をもって入手できるため、他のトレーナーと協力して事前に計画が可能。</p>
        <p>つまりEXバトルの場合、たまたま近くを通りかかったり、始まってから駆けつけても、招待状がない場合は挑戦できません。</p>
        <p>挑戦状を手に入れるには、EXレイドが実施されるジムで、近い時期にレイドに勝利しておくことが必要です。(どの程度の期間なのかは現時点で不明)。</p>
        <p>要はできるだけ多くの場所で、できるだけ頻繁にレイドバトルに勝利しておくことが、招待状ゲットとEXレイド参加の確率を高めることになります。</p>
        <p>(旅行先でたまたまレイド参戦したジムから招待状が届いたりしたら悩むことになりそうです)。</p>
        <p>EXレイドは、今後数週間のうちにも実施される予定。ミュウツー以外のポケモンも、このEXレイドに登場します。</p>
        <p>これまでの伝説のポケモンは、イベントで配布が発表された『詫びルギア』をはじめ、直後に一般解禁されて誰でもゲットの可能性がありました(レイドに勝てる人数が集まる地域なら)。</p>
        <p>しかしミュウツーは、今後少なくとも数週間は、本日横浜スタジアムのイベントで手に入れたトレーナーしか持っていないプレミアム感のある伝説のポケモンになります。</p>
        <p>速報：横浜でミュウツーをゲット！ポケモンGOスタジアム限定、一般解禁はどうなる？ </p>
        <img src="ori_image/88/04c9aee8796a33319dd7b38ea2ae20.jpg" id="127547" width="4800" height="2520">
        <p>EXレイドの発表とあわせて、現在までに一般解禁済みの伝説のポケモンであるルギア、フリーザー、ファイヤー、サンダーのアンコール出現スケジュールも明らかになりました。</p>
        <p>従来発表では、8月15日までサンダー出現、ルギアは「今後しばらく出現」の予定でした。</p>
        <p>新発表によると、この4種は8月15日から9月1日まで継続して出現するとのこと。三鳥を逃して涙を飲んだ皆さんにはリベンジの機会です。</p>
        <p>【ギャラリー】横浜ポケモンGOスタジアムでミュウツー出現 (9枚)</p>
        <div class="video_box" style="height: 180px;">
            <video src="https://video.twimg.com/ext_tw_video/916709455655514112/pu/vid/512x640/o6UWwd7ck0fEmaam.mp4"
             poster="https://pbs.twimg.com/ext_tw_video_thumb/969249655220588544/pu/img/jt6tf8gj9HkEn2E_.jpg"></video>
            <span>2:30</span>
            <i></i>
        </div>
    </div>
</div>
    '''
    article = mock_article()
    article.content = html
    article.embedded_videos = [
        {
            'id': '__test_embed_video___0',
            'sd_url': 'https://video.twimg.com/ext_tw_video/969249655220588544/pu/vid/256x320/OKIAxZ-iHT1Mj-MB.mp4',
            'normal_url': 'https://video.twimg.com/ext_tw_video/969249655220588544/pu/vid/256x320/OKIAxZ-iHT1Mj-MB.mp4',
            'hd_url': 'https://video.twimg.com/ext_tw_video/969249655220588544/pu/vid/256x320/OKIAxZ-iHT1Mj-MB.mp4',
            'cover_image': 'https://pbs.twimg.com/ext_tw_video_thumb/969249655220588544/pu/img/jt6tf8gj9HkEn2E_.jpg',
            'duration_interval': 15,
            'source_type': 1,
            'y_video_id': '',
        },
        {
            'id': '__test_embed_video___1',
            'sd_url': 'https://video.twimg.com/ext_tw_video/916709455655514112/pu/vid/256x320/SyWaA4fFqiY0wd-L.mp4',
            'normal_url': 'https://video.twimg.com/ext_tw_video/916709455655514112/pu/vid/512x640/o6UWwd7ck0fEmaam.mp4',
            'hd_url': 'https://video.twimg.com/ext_tw_video/916709455655514112/pu/vid/512x640/o6UWwd7ck0fEmaam.mp4',
            'cover_image': 'https://pbs.twimg.com/ext_tw_video_thumb/916709455655514112/pu/img/T7xqRNZHygv7MJzp.jpg',
            'duration_interval': 15,
            'source_type': 1,
            'y_video_id': '',
        },
    ]
    return article


def mock_tags_and_hot(items):
    if not items:
        return items
    samples = random.sample(items, len(items) / 2)
    for s in samples:
        if hasattr(s, 'tags'):
            s.tags = random.sample(TAGS, random.randint(1, 2))

    # samples = random.sample(items, len(items) / 2)
    for s in items:
        if hasattr(s, 'comment_count'):
            n = random.randint(0, 10) % 3
            if n == 0:
                s.comment_count = 0
            elif n == 1:
                s.comment_count = random.randint(0, 800)
            elif n == 2:
                s.comment_count = random.randint(999, 10000)

    samples = random.sample(items, 3)
    for s in samples:
        if hasattr(s, 'is_comment_hot'):
            s.is_comment_hot = True
        if hasattr(s, 'display_time'):
            s.display_time = int(time.time() * 1000)


def mock_cover_size():
    return {
        EnumCoverSize.R_16_9_LARGE: ['https://cdn.picknewsforyou.com/other/16_9.jpg'],
        EnumCoverSize.R_16_9_MEDIUM: ['https://cdn.picknewsforyou.com/other/16_9.jpg'],
        EnumCoverSize.R_16_9_5: ['https://cdn.picknewsforyou.com/other/16_95.jpg'],
        EnumCoverSize.R_4_3: ['https://cdn.picknewsforyou.com/other/4_3.jpg'],
        EnumCoverSize.R_4_3_5: ['https://cdn.picknewsforyou.com/other/4_35.jpg'],
        EnumCoverSize.R_1_1: ['https://cdn.picknewsforyou.com/other/1_1.jpg']
    }
