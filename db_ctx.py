# coding=utf-8
"""
简单的数据库访问封装
"""


class DbCtx(object):
    """
    DbCtx:
        数据连接与cursor上下文辅助管理类.
        用法:
            with DbCtx(pool) as (conn, cur):
                cur.execute()
                # etc ..
    """
    def __init__(self, pool):
        """
        :type pool: DBUtils.PooledDB.PooledDB
        """
        self.pool = pool
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = self.pool.connection()
        self.cur = self.conn.cursor()
        return self.conn, self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        self.cur.close()


class DbExec(object):

    def __init__(self, pool):
        """
        :type pool: DBUtils.PooledDB.PooledDB
        """
        self.pool = pool

    def query(self, sql, params=(), only_one=False):
        """
        查询
        :type sql: str
        :type params: tuple
        :type only_one: bool
        :rtype: tuple
        """
        with DbCtx(self.pool) as (conn, cur):
            cur.execute(sql, params)
            if only_one:
                row = cur.fetchone()
                return row
            rows = cur.fetchall()
            return rows

    def execute(self, sql, params=()):
        """
        :type sql: str
        :type params: tuple
        :rtype: tuple
        """
        with DbCtx(self.pool) as (conn, cur):
            n = cur.execute(sql, params)
            conn.commit()
            return n
