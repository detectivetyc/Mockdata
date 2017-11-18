#!/usr/bin/python
# -*- coding:utf-8 -*-

from redis_connection import RedisConnection
from read_configuration import ReadConfiguration
from set_arp import SetArp
from app_log_thread import AppLogThread
from file_log_thread import FileLogThread
from login_log_thread import LoginLogThread
from table import Table
import psutil
import os



def main():
	#print 'memory used: ', psutil.Process(os.getpid()).memory_info().rss
	redis_instance = RedisConnection(ReadConfiguration.redis_port, ReadConfiguration.redis_host, ReadConfiguration.redis_db)
	table = Table()
	SetArp(redis_instance.redis_connection, table)
	buffer = {}
	app_thread = AppLogThread(1, "App-Thread", ReadConfiguration.app_log_num, table, buffer)
	file_thread = FileLogThread(2, "File-Thread", ReadConfiguration.download_log_num, ReadConfiguration.upload_log_num, table, buffer)
	login_thread = LoginLogThread(3, "Login-Thread", ReadConfiguration.login_log_num, table, buffer)

	app_thread.start()
	file_thread.start()
	login_thread.start()

if __name__ == '__main__':
	main() 