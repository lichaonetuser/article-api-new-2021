import os
import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from pyutil.program.conf import Conf


image_conf = Conf(os.path.join(os.path.dirname(__file__), 'conf/image.conf'))


def get_mysql_pool():
    mysql_pool = dict()

    hosts = image_conf.get_values('image_db_write_host')
    for host in hosts:
        conn = {
                'host': host,
                'port': int(image_conf.image_db_write_port),
                'user': image_conf.image_db_write_user,
                'passwd': image_conf.image_db_write_passwd,
                'db': image_conf.image_db_name,
                'cursorclass': DictCursor,
                'charset': 'utf8'
               }
        mysql_pool['image'] = PooledDB(MySQLdb, mincached=0, maxcached=20,
                                       maxshared=20, **conn)
    return mysql_pool
