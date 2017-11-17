import threading
import time
from file_log import FileLog
from redis_connection import RedisConnection
from read_configuration import ReadConfiguration
from aie_volume_log import AieVolumeLog
from user import User
from content_scan import ContentScanLog

class FileLogThread(threading.Thread):
    def __init__(self, threadID, name, download_log_num, upload_log_num, table):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.download_log_num = download_log_num
        self.upload_log_num = upload_log_num
        self.table = table
    def run(self):
        print "Starting " + self.name + '\n'
        run_file_log(self.name, self.download_log_num, self.upload_log_num, self.table)
        print "Ending " + self.name

redis_instance = RedisConnection(ReadConfiguration.redis_port, ReadConfiguration.redis_host, ReadConfiguration.redis_db)
def run_file_log(threadName, download_log_num, upload_log_num, table):
    save_dict = {}
    if download_log_num > 0:
        for i in range(download_log_num):
            user = User(table, 'download')
            file_log = FileLog(redis_instance.redis_connection, table, user)
            file_volume_log = AieVolumeLog(file_log)
            content_scan = ContentScanLog(table, file_log)
            #user = 'User_1'
            file_log.log_process()
            time.sleep(2)
            file_volume_log.log_process()
            time.sleep(2)
            content_scan.log_process()
            del user
            del file_log
            del file_volume_log
            del content_scan
    if upload_log_num > 0 :
        for i in range(upload_log_num):
            user = User(table, 'upload')
            file_log = FileLog(redis_instance.redis_connection, table, user)
            file_volume_log = AieVolumeLog(file_log)
            content_scan = ContentScanLog(table, file_log)
            #user = 'User_1'
            file_log.log_process()
            time.sleep(2)
            file_volume_log.log_process()
            time.sleep(2)
            content_scan.log_process()
            del user
            del file_log
            del file_volume_log
            del content_scan