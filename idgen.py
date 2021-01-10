#!/usr/bin/python
# coding: utf8
import os
import time
import signal
from time import sleep
from multiprocessing import Process, Manager, Queue
import threading
from collections import Counter
from pyutil.program.conf import Conf
from pyutil.user.dal.idgen_dal import IdgenDAL

idgen_dal = None
uids = set()
uids_stats = Counter()
max_concurrent = set()
idgen_conf = Conf(
    os.path.join(os.path.dirname(__file__), 'conf/idgen.conf'))


class TestThread(threading.Thread):
    def __init__(self, q, pid, tid, all_uids, **kws):
        super(self.__class__, self).__init__(**kws)
        self.daemon = True
        self.q = q
        self.pid = pid
        self.tid = tid
        self.all_uids = all_uids

    def run(self, ):
        while True:
            uid = generate('v1.0')
            # print '%s-%s-%s' % (self.pid, self.tid, uid)
            self.q.put((self.pid, self.tid, uid))


class StatsThread(threading.Thread):
    def __init__(self, q, **kws):
        super(self.__class__, self).__init__(**kws)
        self.q = q

    def run(self, ):
        while True:
            pid, tid, uid = self.q.get()
            print_stats(pid, tid, uid)


class TestProcess(Process):
    def __init__(self, queue, pid, **kws):
        super(self.__class__, self).__init__()
        self.queue = queue
        self.ppid = pid

    def run(self, ):
        threads = []
        for i in range(3):
            t = TestThread(self.queue, self.ppid, i, all_uids)
            threads.append(t)
        for t in threads:
            t.start()
            t.join()


def generate(version='v1.0', ):
    global idgen_dal
    global idgen_conf
    if not idgen_dal:
        idgen_dal = IdgenDAL(idgen_conf)
    t = int(time.time())
    bulk_id = get_bulk_id(t, idgen_conf)
    count = idgen_dal.get_count(bulk_id)
    uid = get_uid(t, version, count, idgen_conf)
    return uid


def generate_v2(version='v1.0', conf=idgen_conf):
    # use in diffrent env
    # conf must include db.conf
    idgen_dal = IdgenDAL(conf)

    # need use idgen.conf
    global idgen_conf
    idgen_dal.conf.count_max = idgen_conf.count_max
    idgen_dal.conf.bulk_size = idgen_conf.bulk_size
    idgen_dal.conf.count_length = idgen_conf.count_length

    t = int(time.time())
    bulk_id = get_bulk_id(t, idgen_conf)
    count = idgen_dal.get_count(bulk_id)
    uid = get_uid(t, version, count, idgen_conf)
    return uid


def print_stats(pid, tid, uid):
    global uids
    global uids_stats
    if uid in uids:
        print('error: uid=%s exists' % uid)
    uids.add(uid)
    t = uid[:10]
    uids_stats[t] += 1
    if uids_stats.most_common(1)[0][1] not in max_concurrent:
        max_concurrent.add(uids_stats.most_common(1)[0][1])
        print(uids_stats.most_common(1)[0][1])
    print('%s-%s-%s' % (pid, tid, uid))


def init_db(conf):
    start = time.time()
    dal = IdgenDAL(conf)
    truncate_sql = 'truncate uid_counter'
    dal.execute(truncate_sql)
    values = []
    for i in range(1, int(conf.bulk_size)+1):
        values.append('(%s)' % (i, ))
    insert_sql = 'insert uid_counter (id) values %s' % (
        ', '.join(values), )
    dal.execute(insert_sql)
    print('init time=%.2fs' % (time.time() - start))
    sleep(10)


def get_bulk_id(t, conf):
    return (t % int(conf.bulk_size)) + 1


def get_uid(t, version, count, conf):
    return str(t) + str(count).rjust(int(conf.count_lenght), '0') + \
        str(version)


def exit_signal_handler(sig=None, frame=None):
    os._exit(0)


