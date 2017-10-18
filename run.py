#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import redis
import time
import random
import ConfigParser
from aie_log import Aie_log
from aie_volume_log import Aie_volume_log
from redis_connection import Redis_Connection
from read_configuration import ReadConfiguration
from set_arp import Set_arp
from input_table import Input_table

def read_all_file(table_path, table_list):
	mac_ip_table = Input_table(table_path, ReadConfiguration.mac_ip_table_name)
	mac_ua_table = Input_table(table_path, ReadConfiguration.mac_ua_table_name)
	table_list["mac-ip"] = mac_ip_table
	table_list["mac-ua"] = mac_ua_table
	if ReadConfiguration.mode == "file":
		file_table_path = table_path + "file/"
		download_ip_service_table = Input_table(file_table_path, ReadConfiguration.donwload_ip_service_table_name)
		download_service_appname_table = Input_table(file_table_path, ReadConfiguration.donwload_service_appname_table_name)
		download_ip_host_table = Input_table(file_table_path, ReadConfiguration.donwload_ip_host_table_name)
		download_appname_url_table = Input_table(file_table_path, ReadConfiguration.donwload_appname_url_table_name)
		download_appname_rspcode_table = Input_table(file_table_path, ReadConfiguration.donwload_appname_rspcode_table_name)
		download_appname_sigid_table = Input_table(file_table_path, ReadConfiguration.donwload_appname_sigid_table_name)
		table_list["download-ip-service"] = download_ip_service_table
		table_list["download-service-appname"] = download_service_appname_table
		table_list["download-ip-host"] = download_ip_host_table
		table_list["download-appname-url"] = download_appname_url_table
		table_list["download-appname-rspcode"] = download_appname_rspcode_table
		table_list["download-appname-sigid"] = download_appname_sigid_table		
	else:
		app_login_table_path = table_path + "app_login/"
		service_appname_table = Input_table(app_login_table_path, ReadConfiguration.service_appname_table_name)
		ip_service_table = Input_table(app_login_table_path, ReadConfiguration.ip_service_table_name)
		ip_host_table = Input_table(app_login_table_path, ReadConfiguration.ip_host_table_name)
		service_url_table = Input_table(app_login_table_path, ReadConfiguration.service_url_table_name)
		service_rspcode_table = Input_table(app_login_table_path, ReadConfiguration.service_rspcode_table_name)
		service_sigid_table = Input_table(app_login_table_path, ReadConfiguration.service_sigid_table_name)
		table_list["ip-service"] = ip_service_table
		table_list["service-appname"] = service_appname_table
		table_list["ip-host"] = ip_host_table
		table_list["service-url"] = service_url_table
		table_list["service-rspcode"] = service_rspcode_table
		table_list["service-sigid"] = service_sigid_table


def main():
	table_path = "MockDataInput/"
	table_list = {}
	redis_instance = Redis_Connection(ReadConfiguration.redis_port, ReadConfiguration.redis_host, ReadConfiguration.redis_db)
	read_all_file(table_path, table_list)
	Set_arp(table_list["mac-ip"], redis_instance.redis_connection)
	for i in range(ReadConfiguration.num):
		aie_log = Aie_log(ReadConfiguration.mode, redis_instance.redis_connection, read_conf, table_path, table_list)
		retval = aie_log.log_init()
		if retval == -1:
			sys.exit("Something wrong with aie log")
			return
		aie_volume_log = Aie_volume_log(aie_log)
		retval = aie_volume_log.log_init()
		if retval == -1:
			sys.exit("Something wrong with aie_volume log")
			return 

if __name__ == '__main__':
	main() 