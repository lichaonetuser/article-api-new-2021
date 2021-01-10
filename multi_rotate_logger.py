# -*- coding: utf-8 -*-

import time
from logging.handlers import TimedRotatingFileHandler
import os
import fcntl


class MultiProcessRotatingFileHandler(TimedRotatingFileHandler):
    """
    handler for logging to a file for multi process...
    """

    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False):
        TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay, utc)
        if not os.path.exists(self.baseFilename):
            self.dev, self.ino = -1, -1
        else:
            stat = os.stat(self.baseFilename)
            self.dev, self.ino = stat.st_dev, stat.st_ino

    def cumpute_next_time(self):
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstNow = time.localtime(currentTime)[-1]
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    newRolloverAt = newRolloverAt - 3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    newRolloverAt = newRolloverAt + 3600
        self.rolloverAt = newRolloverAt

    def get_new_file(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.mode = 'a'
        self.stream = self._open()
        stat = os.stat(self.baseFilename)
        self.dev, self.ino = stat.st_dev, stat.st_ino

    def doRollover(self):
        #rotate
        with open(self.baseFilename + '.lock', 'a') as f:
            try:
                fcntl.flock(f, fcntl.LOCK_EX)
                if not os.path.exists(self.baseFilename):
                    f_new = open(self.baseFilename, 'w')
                    f_new.close()
                stat = os.stat(self.baseFilename)
                if self.dev != stat.st_dev or self.ino != stat.st_ino:
                    # stream is not the same.Log file must be rotated already.
                    self.get_new_file()
                    self.cumpute_next_time()
                else:
                    TimedRotatingFileHandler.doRollover(self)
                    self.get_new_file()
            except:
                pass
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
