import threading
import psutil
import time
from login_log import LoginLog
from redis_connection import RedisConnection
from read_configuration import ReadConfiguration
from aie_volume_log import AieVolumeLog
from user import User

class LoginLogThread(threading.Thread):
    def __init__(self, threadID, name, log_num, table, buffer):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.log_num = log_num
        self.table = table
        self.buffer = buffer
    def run(self):
        print "Starting " + self.name + '\n'
        run_login_log(self.name, self.log_num, self.table, self.buffer)
        print "Ending " + self.name

redis_instance = RedisConnection(ReadConfiguration.redis_port, ReadConfiguration.redis_host, ReadConfiguration.redis_db)
def run_login_log(threadName, log_num, table, buffer):
    for i in range(log_num):
        #print 'memory used: ', psutil.Process(os.getpid()).memory_info().rss
        user = User(table)
        login_log = LoginLog(redis_instance.redis_connection, table, user)
        login_volume_log = AieVolumeLog(login_log)
        #user = 'User_2'
        login_log.log_process(buffer)
        time.sleep(2)
        login_volume_log.log_process()
        del user
        del login_log
        del login_volume_log