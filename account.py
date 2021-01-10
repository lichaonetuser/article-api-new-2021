# code=utf-8

import time
import requests
import json
import tweepy
from pyutil.program.exception import MyException


class Birthday:
    DEFAULT = '01/01/1990'


class Gender:
    MALE = 1
    FEMALE = 2
    UNKNOWN = 0


class Platform:
    FACEBOOK = 0
    TWITTER = 1
    GOOGLE = 2
    LINE = 3
    WECHAT = 4
    PUSIC = 5
    APPLE = 7
    UNKNOWN = -1


class BaseHandler(object):
    def __init__(self, conf, **kwargs):
        self.conf = conf
        self.token = kwargs.get('token', '')
        self.secret = kwargs.get('secret', '')


class Facebook(BaseHandler):

    def __init__(self, conf, **kwargs):
        super(Facebook, self).__init__(conf, **kwargs)

    def get_user_profile(self, app_id='myfm'):
        params = {
            'access_token': self.token,
            'fields': 'email,name,birthday,gender,picture'
        }
        rs = requests.get(
            self.conf.facebook_me_uri,
            params=params,
        )
        if rs.status_code != requests.codes.ok:
            raise Exception('Reqeust facebook failed.')
        profile = json.loads(rs.text)
        format_profile = self.__format_profile(profile)
        return format_profile

    def __format_profile(self, user_profile):
        format_profile = dict()
        format_profile['screen_name'] = user_profile['name']

        gender_selector = {
            "male": 1,
            "female": 2
        }
        gender = gender_selector.get(user_profile.get('gender', ''), 0)
        format_profile['gender'] = gender
        format_profile['email'] = user_profile.get('email', '')
        format_profile['avatar_url'] = user_profile['picture']['data']['url']
        birthday = user_profile.get('birthday', '')
        if birthday:
            format_profile['birthday'] = int(time.mktime(
                time.strptime(birthday, '%m/%d/%Y')))
        format_profile['platform_uid'] = str(user_profile['id'])
        # need extra permission to get contact info
        format_profile['phone'] = ''
        format_profile['address'] = ''
        format_profile['platform'] = 0
        return format_profile


class Twitter(BaseHandler):
    def __init__(self, conf, **kwargs):
        super(Twitter, self).__init__(conf, **kwargs)

    def get_user_profile(self, app_id='myfm'):
        if 'live' in app_id:
            consumer_key = self.conf.live_twitter_consumer_key
            consumer_secret = self.conf.live_twitter_consumer_secret
        else:
            consumer_key = self.conf.twitter_consumer_key
            consumer_secret = self.conf.twitter_consumer_secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth.set_access_token(self.token, self.secret)
        api = tweepy.API(auth)
        try:
            raw_info = api.me()
        except Exception as e:
            raise e
        else:
            format_profile = self.__format_profile(raw_info)
            return format_profile

    @staticmethod
    def __format_profile(raw_info):
        format_profile = dict()
        format_profile['platform_uid'] = str(raw_info.id)
        format_profile['screen_name'] = raw_info.screen_name
        format_profile['avatar_url'] = raw_info.profile_image_url
        format_profile['email'] = ''
        format_profile['gender'] = 0
        birthday = ''
        birthday = birthday if birthday else '01/01/1990'
        format_profile['birthday'] = int(time.mktime(
            time.strptime(birthday, '%m/%d/%Y')))
        format_profile['phone'] = ''
        format_profile['address'] = ''
        format_profile['platform'] = 1
        return format_profile


def get_handler(platform):
    if platform == Platform.FACEBOOK:
        return Facebook
    elif platform == Platform.TWITTER:
        return Twitter
    else:
        raise MyException('unknown platform')
