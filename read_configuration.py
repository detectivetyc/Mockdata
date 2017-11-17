#!/usr/bin/python
# -*- coding:utf-8 -*-
import yaml

class ReadConfiguration:

	mock_conf_yaml = open("MockDataInput/mock_conf.yaml")
	mock_conf = yaml.load(mock_conf_yaml)
	#redis configuration
	redis_dict = mock_conf['redis']
	aie_list_name = redis_dict['aie_list_name']
	aie_volume_list_name = redis_dict['aie_volume_list_name']
	content_scan_list_name = redis_dict['content_scan_list_name']
	redis_port = redis_dict['redis_port']
	redis_host = redis_dict['redis_host']
	redis_db = redis_dict['redis_db']
	#basic
	app_log_num = mock_conf['log_num']['app_log_num']
	login_log_num = mock_conf['log_num']['login_log_num']
	download_log_num = mock_conf['log_num']['download_log_num']
	upload_log_num = mock_conf['log_num']['upload_log_num']
	#sql input file name
	sql_dict = mock_conf['sql']
	activity_sql_name = sql_dict['activity']
	context_sql_name = sql_dict['context']
	element_sql_name = sql_dict['element']
	service_sql_name = sql_dict['service']
	#Input user table
	user_table_path = mock_conf['user_table']['path']
	user_table_name = mock_conf['user_table']['name']
	#Input device table
	device_table_path = mock_conf['device_table']['path']
	device_table_name = mock_conf['device_table']['name']
	#Input app table
	app_table_path = mock_conf['app_table']['path']
	app_table_name = mock_conf['app_table']['name']
	#Download table
	download_table_path = mock_conf['download_table']['path']
	download_table_name = mock_conf['download_table']['name']
	#Upload table
	upload_table_path = mock_conf['upload_table']['path']
	upload_table_name = mock_conf['upload_table']['name']
	#Time set
	days = mock_conf['time']['days']
	hours = mock_conf['time']['hours']
	mins = mock_conf['time']['mins']
	#GW & AIE
	gw_id = mock_conf['gw_id']
	aie_id = mock_conf['aie_id']
	#Output Path
	output_path = mock_conf['Output']['path']