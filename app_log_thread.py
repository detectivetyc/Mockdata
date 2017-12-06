import threading
import psutil
import time
from app_log import AppLog
from redis_connection import RedisConnection
from read_configuration import ReadConfiguration
from aie_volume_log import AieVolumeLog
from user import User
from check_es import CheckES

class AppLogThread(threading.Thread):
    def __init__(self, threadID, name, log_num, table, buffer):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.log_num = log_num
        self.table = table
        self.buffer = buffer
    def run(self):
        print "Starting " + self.name + '\n'
        run_app_log(self.name, self.log_num, self.table, self.buffer)
        print "Ending " + self.name

redis_instance = RedisConnection(ReadConfiguration.redis_port, ReadConfiguration.redis_host, ReadConfiguration.redis_db)
def run_app_log(threadName, log_num, table, buffer):
    for i in range(log_num):
        #print 'memory used: ', psutil.Process(os.getpid()).memory_info().rss
        user = User(table)
        app_log = AppLog(redis_instance.redis_connection, table, user)
        app_volume_log = AieVolumeLog(app_log)
        app_log.log_process(buffer)
        app_volume_log.log_process()
        checkES = CheckES('http://dev-ds.holonetsecurity.com:9200', app_log)
        time.sleep(1)
        total = checkES.check_log_exist()
        print total
        del user
        del app_log
        del app_volume_log


