# coding=utf8
from pyutil.program.db_pool import BaseDAL
from pyutil.constants import AppIds
from api.feedback.types import Feedback


class FeedbackBaseDAL(BaseDAL):
    def __init__(self, db_pool, app_id):
        super(FeedbackBaseDAL, self).__init__(db_pool.get('feedback'))
        self.table_name = AppIds.Feedback_Tables.get(app_id, AppIds.Default_Feedback_Table)


class FeedbackDAL(FeedbackBaseDAL):
    def get_feedback(self, where):
        rs = self.fetchall(
            self.table_name,
            keys=['*', ],
            where=where,
        )
        return [Feedback(r) for r in rs]

    def get_feedbacks(self, where, limit):
        rs = self.fetchall(
            self.table_name,
            keys=['*', ],
            where=where,
            limit=limit,
            order_by='mtime asc'
        )
        return [Feedback(r) for r in rs]

    def get_feedbacks_by_sql(self, uid, unique_device_id):
        sql_prefix = 'select * from %s ' % self.table_name
        sql = sql_prefix + 'where uid=%s or unique_device_id=%s ' \
                           'order by id desc limit 100'
        self.execute(sql, *(uid, unique_device_id, ))
        rs = self.cursor.fetchall()
        return [Feedback(r) for r in rs][::-1]

    def get_unread_feedbacks_by_sql(self, uid, unique_device_id):
        sql_prefix = 'select * from %s ' % self.table_name
        sql = sql_prefix + 'where (uid=%s or unique_device_id=%s) ' \
                           'and is_read=0 order by id desc limit 100'
        self.execute(sql, *(uid, unique_device_id, ))
        rs = self.cursor.fetchall()
        return [Feedback(r) for r in rs][::-1]

    def update_feedback_read_status(self, uid, unique_device_id):
        sql_prefix = 'update %s set is_read=1 ' % self.table_name
        sql = sql_prefix + \
            'where is_read=0 and (uid=%s or unique_device_id=%s)'
        return self.execute(sql, *(uid, unique_device_id, ))

    def insert_feedback(self, info):
        return self.insert(
            self.table_name,
            info=info
        )

    def update_feedback(self, info, where):
        return self.update(
            self.table_name,
            info,
            **where
        )
