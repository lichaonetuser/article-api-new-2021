# coding=utf8
import MySQLdb
import codecs

codecs.register(
    lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)


def get_where_op(k, v=''):
    '''
    >>> get_where_op('a')
    'a = %s'
    >>> get_where_op('a__ne')
    'a != %s'
    >>> get_where_op('a__lt')
    'a < %s'
    >>> get_where_op('a__isnull', False)
    'a is not null'
    >>> get_where_op('a__regexp')
    'a regexp %s'
    >>> get_where_op('a', [1, 2])
    'a in %s'
    '''

    op_map = dict(
        ne='!=',
        lt='<',
        lte='<',
        gt='>',
        gte='>=',
        isnull='isnull',
        regexp='regexp'
        )

    parts = k.rsplit('__', 1)
    if len(parts) == 2:
        k, op = parts
        op = op_map[op]
    else:
        k = parts[0]
        op = 'in' if isinstance(v, (list, tuple)) else '='

    if op == 'isnull':
        return '%s is %s' % (k, 'null' if v else 'not null')
    else:
        return '%s %s %%s' % (k, op)


def get_where_sql(where):
    '''
    >>> get_where_sql(['a.b', 'c'])
    'a.b = %s and c = %s'
    >>> get_where_sql(['a__ne'])
    'a != %s'
    >>> get_where_sql(dict(a=[1,2], b='x'))
    'a in %s and b = %s'
    '''
    if isinstance(where, (list, tuple)):
        where_keys = where
        where = {x: '' for x in where}
    else:
        where_keys = where.keys()
    return ' and '.join(get_where_op(k, where[k]) for k in where_keys)


def get_insert_sql(
    table, keys, on_duplicate_update=False,
        ignore=False, dup_unupdate_keys=[]):
    '''
    >>> get_insert_sql('foo', ['a', 'b'])
    'insert into foo (a, b) values (%s, %s)'
    >>> get_insert_sql('foo', ['a', 'b'], on_duplicate_update=True)
    'insert into foo (a, b) values (%s, %s) \
ON DUPLICATE KEY UPDATE a=values(a), b=values(b)'
    >>> get_insert_sql(
    ...     'foo', ['a', 'b'], on_duplicate_update=True,
    ...     dup_unupdate_keys=['a', ])
    'insert into foo (a, b) values (%s, %s) \
ON DUPLICATE KEY UPDATE b=values(b)'
    '''
    sql = 'insert into %s (%s) values (%s)' % (
        table, ', '.join(keys), ', '.join(['%s'] * len(keys)))
    if on_duplicate_update:
        odu_clause = ' ON DUPLICATE KEY UPDATE %s' % (
            ', '.join(
                '%s=values(%s)' % (k, k) for k in keys
                if k not in dup_unupdate_keys))
        sql = sql + odu_clause
    return sql


def get_update_sql(table, update_keys, where):
    '''
    >>> get_update_sql('foo', ['a', 'b'], dict(a=1, b=2))
    'update foo set a=%s, b=%s where a = %s and b = %s'
    >>> get_update_sql('foo', ['a'], dict(id__isnull=True))
    'update foo set a=%s where id is null'
    '''
    sql = 'update %s set %s where %s' % (
        table,
        ', '.join(x + '=%s' for x in update_keys),
        get_where_sql(where),
        )
    return sql


def get_delete_sql(table, where):
    '''
    >>> get_delete_sql('foo', dict(a=1, b=2))
    'delete from foo where a = %s and b = %s'
    >>> get_delete_sql('foo', dict(id__isnull=True))
    'delete from foo where id is null'
    '''
    sql = 'delete from %s where %s' % (
        table,
        get_where_sql(where),
        )
    return sql


def get_select_sql(
        table, keys, where=None, extra=None, order_by=None, limit=None):
    '''
    >>> get_select_sql('foo', ['a', 'b'], order_by='a asc', limit=1)
    'select a, b from foo order by a asc limit 1'
    >>> get_select_sql('foo', ['a', 'b'], extra="order by a asc", limit=1)
    'select a, b from foo order by a asc limit 1'
    >>> get_select_sql('foo', ['a', 'b'], ['b', 'c'])
    'select a, b from foo where b = %s and c = %s'
    >>> get_select_sql('foo', ['a', 'b'], where=dict(a__ne=5, b__isnull=True))
    'select a, b from foo where b is null and a != %s'
    '''

    sql = 'select %s from %s' % (', '.join(keys), table)
    if where:
        sql += ' where ' + get_where_sql(where)
    if order_by:
        sql += ' order by ' + order_by
    if extra:
        sql += ' ' + extra
    if limit:
        sql += ' limit %s' % limit
    return sql


def unfold_one(lst):
    if isinstance(lst, (list, tuple)) and len(lst) == 1:
        return lst[0]
    else:
        return lst


class DAL(object):
    def __init__(self, pooled_db):
        self.pooled_db = pooled_db
        self.cursor = None
        self.conn = None

    def __del__(self):
        self.close()

    def open(self):
        conn = self.pooled_db.connection()
        self.conn = conn
        self.cursor = conn.cursor()
        self.cursor.connection.autocommit(True)

    def get_cursor(self):
        if not self.cursor:
            self.open()
        return self.cursor

    def execute(self, sql_fmt, *params):
        retry = 0
        while True:
            retry += 1
            try:
                # cursor = self.get_cursor() // 老代码
                self.get_cursor()
                self.cursor.execute(sql_fmt, params)
                break
            except:
                self.close()
                if retry >= 2:
                    raise

    def close(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.conn:
            self.conn.close()
            self.conn = None

    # 需要支持事务
    def begin(self, ):
        self.get_cursor()
        self.conn.begin()

    def commit(self, ):
        self.get_cursor()
        self.conn.commit()
        self.close()

    def rollback(self, ):
        self.get_cursor()
        self.conn.rollback()
        self.close()


class BaseDAL(DAL):
    def insert(
        self, table, info, on_duplicate_update=False,
            unique_keys={}, dup_unupdate_keys=[]):
        if not info:
            return None, 'no values'
        if unique_keys:
            rs = self.fetchone(table, ['id', ], where=unique_keys)
            if rs:
                return rs['id'], 'already exist, not insert'
        try:
            sql = get_insert_sql(
                table, info.keys(), on_duplicate_update,
                dup_unupdate_keys=dup_unupdate_keys)
            self.execute(sql, *info.values())
            return self.cursor.connection.insert_id(), 'new insert'
        except MySQLdb.IntegrityError:
            if unique_keys:
                rs = self.fetchone(table, ['id', ], where=unique_keys)
                if rs:
                    return rs['id'], 'already exist, insert error'
            raise
        except:
            raise

    # 专门给song使用的, 其他的表，不可使用
    def insert2(
        self, table, info, on_duplicate_update=False,
            unique_keys={}, dup_unupdate_keys=[]):
        if not info:
            return None, 'no values'
        if unique_keys:
            rs = self.fetchone(table, ['sid', ], where=unique_keys)
            if rs:
                return rs['sid'], 'already exist, not insert'
        try:
            sql = get_insert_sql(
                table, info.keys(), on_duplicate_update,
                dup_unupdate_keys=dup_unupdate_keys)
            self.execute(sql, *info.values())
            return self.cursor.connection.insert_id(), 'new insert'
        except MySQLdb.IntegrityError:
            if unique_keys:
                rs = self.fetchone(table, ['sid', ], where=unique_keys)
                if rs:
                    return rs['sid'], 'already exist, insert error'
            raise
        except:
            raise

    def update(self, table, info, **where):
        if 'where' in where:
            where = where['where']
        if not info or not where:
            return
        # workaround: MySQLdb对于只有一个元素的list执行in操作有bug
        where = {k: unfold_one(v) for k, v in where.iteritems()}
        # isnull没有%s, 故需从values中去掉
        where_values = [
            v for k, v in where.iteritems()
            if not k.endswith('__isnull')]
        sql = get_update_sql(table, info.keys(), where)
        self.execute(sql, *(info.values() + where_values))

    def delete(self, table, **where):
        if 'where' in where:
            where = where['where']
        if not where:
            return
        # workaround: MySQLdb对于只有一个元素的list执行in操作有bug
        where = {k: unfold_one(v) for k, v in where.iteritems()}
        # isnull没有%s, 故需从values中去掉
        where_values = [
            v for k, v in where.iteritems()
            if not k.endswith('__isnull')]
        sql = get_delete_sql(table, where)
        self.execute(sql, *where_values)

    def _fetch(self, one, table, keys, order_by=None, limit=None, **where):
        if 'where' in where:
            where = where['where']
        # workaround: MySQLdb对于只有一个元素的list执行in操作有bug
        where = {k: unfold_one(v) for k, v in where.iteritems()}
        sql = get_select_sql(
            table, keys, where, order_by=order_by, limit=limit)
        # isnull没有%s, 故需从values中去掉
        where_values = [
            v for k, v in where.iteritems() if not k.endswith('__isnull')]
        self.execute(sql, *where_values)
        if one:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    def fetchone(self, table, keys, order_by=None, **where):
        result = self._fetch(
            True, table, keys, order_by=order_by, limit=1, **where)
        return result

    def fetchall(self, table, keys, order_by=None, limit=None, **where):
        result = self._fetch(
            False, table, keys, order_by=order_by, limit=limit, **where)
        return result

    def fetch_by_sql(self, sql, one=False):
        self.execute(sql)
        if one:
            result = self.cursor.fetchone()
        else:
            result = self.cursor.fetchall()
        return result


def __autocommit_on(sender, **kwargs):
    kwargs['connection'].connection.autocommit(True)


def set_autocommit():
    """
    example:

    from pyutil.program.db import set_autocommit
    set_autocommit()

    """
    from django.db.backends.signals import connection_created
    connection_created.connect(__autocommit_on)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
