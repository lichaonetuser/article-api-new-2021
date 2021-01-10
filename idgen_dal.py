#!/usr/bin/env python
# coding=utf8
import logging
import MySQLdb


class IdNotExistException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class IdgenDAL():
    def __init__(self, conf):
        self.db = MySQLdb.connect(
            host=conf.idgen_db_write_host,
            user=conf.idgen_db_write_user,
            passwd=conf.idgen_db_write_passwd,
            db=conf.idgen_db_name,
            port=int(conf.idgen_db_write_port)
            )
        self.db.autocommit(False)
        self.cursor = self.db.cursor()
        self.conf = conf

    def execute(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    def open(self, ):
        if not self.cursor:
            self.cursor = self.db.cursor()

    def get_count(self, bulk_id):
        # 需要使用事务来处理
        conn = MySQLdb.connect(
            host=self.conf.idgen_db_write_host,
            user=self.conf.idgen_db_write_user,
            passwd=self.conf.idgen_db_write_passwd,
            db=self.conf.idgen_db_name,
            port=int(self.conf.idgen_db_write_port)
            )
        conn.autocommit(False)
        # import pdb; pdb.set_trace()
        with conn:
            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            try:
                sql = 'select * from uid_counter where id=%s for update' % (
                    bulk_id)
                cursor.execute(sql)
                rs = cursor.fetchone()
                if rs:
                    count = (rs['count'] + 1) % int(self.conf.count_max)
                    update_sql = \
                        'update uid_counter set count= %s where id = %s' % (
                            count, bulk_id)
                    cursor.execute(update_sql)
                else:
                    raise IdNotExistException(
                        'id=%s not exist' % bulk_id)
                conn.commit()
                return count
            except Exception as e:
                logging.error('e = %s' % e)
                conn.rollback()
