# coding=utf-8

from mongoengine import Document, IntField, StringField, DateTimeField, ListField, BooleanField, DictField
from api.utils.api import APIModel


class RankList(Document):
    meta = {
        'db_alias': 'sport_api',
        'collection': 'sport_season_player_stats',
        'indexes': ['season_id'],
        'strict': False,
    }

    season_id = IntField()
    data = DictField()


class TeamRankList(Document):
    meta = {
        'db_alias': 'sport_api',
        'collection': 'sport_season_team_stats',
        'indexes': ['season_id'],
        'strict': False,
    }

    season_id = IntField()
    team_ranking = ListField(DictField())


class SeasonSchedule(Document):
    meta = {
        'db_alias': 'sport_api',
        'collection': 'sport_season_schedule',
        'indexes': ['season_id', 'season_schedule_id'],
        'strict': False,
    }

    season_id = IntField()
    season_schedule_id = IntField()
    data = DictField()
