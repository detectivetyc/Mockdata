#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
from aie_log import AieLog
from aie_volume_log import Aie_volume_log
from app_log import AppLog
from redis_connection import Redis_Connection
from read_configuration import ReadConfiguration
from set_arp import Set_arp
from read_file import ReadFile
from file_log import FileLog




def main():
	redis_instance = Redis_Connection(ReadConfiguration.redis_port, ReadConfiguration.redis_host, ReadConfiguration.redis_db)
	Set_arp(ReadFile.mac_ip_table, redis_instance.redis_connection)
	#generate app log
	app_log = AppLog(redis_instance.redis_connection)
	app_log.log_process()
	#generate file log
	file_log = FileLog(redis_instance.redis_connection)
	file_log.log_process()
	#generate login log
if __name__ == '__main__':
	main() 