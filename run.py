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
from read_configuration import Read_Configuration
from set_arp import Set_arp
from input_table import Input_table

def read_all_file(table_path, table_list, read_conf):
	mac_ip_table = Input_table(table_path, read_conf.mac_ip_table_name)
	service_sigid_table = Input_table(table_path, read_conf.service_sigid_table_name)
	ip_service_table = Input_table(table_path, read_conf.ip_service_table_name)
	ip_host_table = Input_table(table_path, read_conf.ip_host_table_name)
	service_url_table = Input_table(table_path, read_conf.service_url_table_name)
	service_rspcode_table = Input_table(table_path, read_conf.service_rspcode_table_name)
	sigid_appname_table = Input_table(table_path, read_conf.sigid_appname_table_name)
	mac_ua_table = Input_table(table_path, read_conf.mac_ua_table_name)
	table_list["mac-ip"] = mac_ip_table
	table_list["ip-service"] = ip_service_table
	table_list["service-sigid"] = service_sigid_table
	table_list["ip-host"] = ip_host_table
	table_list["service-url"] = service_url_table
	table_list["service-rspcode"] = service_rspcode_table
	table_list["sigid-appname"] = sigid_appname_table
	table_list["mac-ua"] = mac_ua_table

def main():
	table_path = "/Users/yuchentang/Documents/pythonDoc"
	config_path = "/Users/yuchentang/Documents/PythonWorkSpace/MockData/"
	config_filename = "mock_data.conf"
	table_list = {}
	read_conf = Read_Configuration(config_path, config_filename)
	redis_instance = Redis_Connection(read_conf.redis_port, read_conf.redis_host, read_conf.redis_db)
	read_all_file(table_path, table_list, read_conf)
	set_arp = Set_arp(table_list["mac-ip"], redis_instance.redis_connection)
	for i in range(read_conf.num):
		aie_log = Aie_log(read_conf.mode, redis_instance.redis_connection, read_conf, table_path, table_list)
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