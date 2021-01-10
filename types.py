# coding=utf-8

platform_choices = (
    (0, 'facebook'),
    (1, 'twitter'),
    (2, 'google'),
    (3, 'line'),
    (4, 'wechat'),
    (5, 'pusic'),
    )

is_active_choices = (
    (0, '未放出'),
    (1, '放出'),
    )

gender_choices = (
    (0, '未知'),
    (1, '男'),
    (2, '女'),
    )

# 最多在线设备数
MAX_DEVICES_ONLINE = 2

# 登陆过期时间
TOKEN_EXPIRE_AFTER = 5184000

class User():
    TYPE_UID = 'uid'
    TYPE_UNIQUE_DEVICE_ID = 'udid'

class LoginStatus:
    OK = 0
    FACEBOOK_TOKEN_EXPIRE = 1
    TWITTER_TOKEN_EXPIRE = 2
    FORCE_LOGOUT = 255
    UNKNOWN_EXPIRE = -1
    UNKNOWN_REASON = -2

    MESSAGE = {
        FACEBOOK_TOKEN_EXPIRE: {
            'ja': 'Facebook登録時限が超えて、クリックして再ログインしてください.',
            'zh-hans': 'Facebook登陆已过期，点击前往重新登录.',
            'zh-hant': 'Facebook登錄已過期, 點擊前往重新登陸.',
            'ko': 'Facebook로그인 다시 로그인을하기 위해 클릭을 통해, 만료되었습니다.',
            'en': 'Facebook login expired. Tap OK to login again.'
        },
        TWITTER_TOKEN_EXPIRE: {
            'ja': 'Twitter登録時限が超えて、クリックして再ログインしてください.',
            'zh-hans': 'Twitter登陆已过期，点击前往重新登录.',
            'zh-hant': 'Twitter登錄已過期, 點擊前往重新登陸.',
            'ko': 'Twitter로그인 다시 로그인을하기 위해 클릭을 통해, 만료되었습니다.',
            'en': 'Twitter login expired. Tap OK to login again.'
        },
        UNKNOWN_EXPIRE: {
            'ja': '登録時限が超えて、クリックして再ログインしてください.',
            'zh-hans': '登陆已过期，点击前往重新登录.',
            'zh-hant': '登錄已過期, 點擊前往重新登陸.',
            'ko': '로그인 다시 로그인을하기 위해 클릭을 통해, 만료되었습니다.',
            'en': 'Login expired. Tap OK to login again.'
        },
        FORCE_LOGOUT: {
            'ja': 'アカウントが他のアプリ使用されるので、再ログインしてください.',
            'zh-hans': '您的账号已在其他设备使用，请重新登录.',
            'zh-hant': '您的賬號已在其他設備使用，請重新登錄.',
            'ko': '계정이 다른 장치에왔다, 다시 로그인하시기 바랍니다.',
            'en': 'Your account has been used on other device. \
                   Please login again.'
        }
    }
