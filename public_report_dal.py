# coding=utf8
from datetime import datetime
from pyutil.program.db_pool import BaseDAL
from api.memcached_pool import memcache_cli
from pyutil.program.cache import Cache, pickle_ss
cache_func = Cache(memcache_cli, serializer=pickle_ss)


class PublicReportDAL(BaseDAL):
    def __init__(self, db_pool):
        super(PublicReportDAL, self).__init__(db_pool.get('public_report'))

    def insert_public_report(self, info, table='article_public_report', on_duplicate_update=True):
        return self.insert(
            table,
            info=info,
            on_duplicate_update=on_duplicate_update,
            dup_unupdate_keys=['ctime']
        )

    def insert_or_update_report_count(self, item_id, report_type):
        try:
            return self.insert(
                'article_report_count',
                info={"item_id": item_id, "ctime": datetime.now(), "report_type": report_type, "count": 1},
                on_duplicate_update=False
            )
        except:
            sql = """
                update article_report_count set count=count + 1
                where item_id = %s and report_type = %s
                """
            return self.execute(sql, item_id, report_type)
