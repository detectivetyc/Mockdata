#!/usr/bin/python
# -*- coding:utf-8 -*-

import random
from output import output
from datetime import datetime
from datetime import timedelta
from read_configuration import ReadConfiguration
from read_file import ReadFile


class AieLog():

	def __init__(self, redis_connection):
		self.redis_connection = redis_connection

	def log_process(self):
		# timestamp
		self.timestamp = self.generate_timestamp()
		# gw_id
		self.gw_id = "G011609F3C98"
		# aie_id
		self.aie_id = "HOLOFLOW_IN_TEST"
		# mac, src_ip, dst_ip, service got in get_ip_port_session()
		# ip_seg
		self.ip_seg = self.get_ip_port_session()
		# log_tyep
		self.log_type = 1
		# log_version
		self.log_version = 1
		# log_id
		self.log_id = random.randint(1, 999999)
		# log_seq_num
		self.log_seq_num = 0
		# log_lf
		self.log_lf = 0
		# user agent
		self.ua = self.get_ua()
		# method
		self.method = ["POST", "PUT", "GET", "CONNECT", "HEAD", "OPTIONS", "TRACE"]  # hard coded
		# appname
		self.appname = self.get_appname()
		# download-sigid
		self.sigid = self.get_sigid()
		# download-host
		self.host = self.get_host()
		# url
		self.url = self.get_url()
		# rsp_code
		self.rsp_code = self.get_rspcode()
		#log message head
		self.message_head = self.message_head_process()
		#log message body
		self.message_body = self.message_body_process()
		#log assemble
		self.log = self.message_head + " " + self.message_body
		#push log into redis server
		self.push_log()

	def generate_timestamp(self):
		time_show = datetime.now()
		delta = timedelta(days = ReadConfiguration.days_delta, minutes = ReadConfiguration.minutes_delta)
		time_show = time_show + delta
		return time_show.strftime("%Y-%m-%dT%H:%M:%S")

	#Should rewrite in file/login log class
	def get_ip_port_session(self):
		# src
		self.mac = random.choice(ReadFile.mac_ip_table.keys)
		self.src_ip = ReadFile.mac_ip_table.dict[self.mac]
		self.src_port = random.randint(1, 65535)
		# dst
		self.dst_ip = random.choice(ReadFile.app_ip_service_table.keys)
		self.service = ReadFile.app_ip_service_table.dict[self.dst_ip]
		self.dst_port = random.randint(1, 65535)
		self.session_id = random.randint(1, 999999)
		ip_seg = self.src_ip + ":" + str(self.src_port) + ":"
		ip_seg += self.dst_ip + ":" + str(self.dst_port) + ":" + str(self.session_id)
		return ip_seg

	# Should rewrite in file/login log class
	def get_ua(self):
		return ReadFile.mac_ua_table.dict[self.mac]

	# Should rewrite in file/login log class
	def get_appname(self):
		return ReadFile.app_service_appname_table.dict[self.service]

	# Should rewrite in file/login log class
	def get_sigid(self):
		return ReadFile.app_service_sigid_table.dict[self.service]

	# Should rewrite in file/login log class
	def get_host(self):
		return ReadFile.app_ip_host_table.dict[self.dst_ip]

	# Should rewrite in file/login log class
	def get_url(self):
		return ReadFile.app_service_url_table.dict[self.service]

	# Should rewrite in file/login log class
	def get_rspcode(self):
		return ReadFile.app_service_rspcode_table.dict[self.service]

	def message_body_process(self):
		#handle message_body at child class
		#should be rewritten at child class
		body = "{"
		body += "}"
		return body

	def message_head_process(self):
		head = str(self.timestamp) + " " + self.gw_id + " " + str(self.aie_id) + " " + str(self.ip_seg) \
				+ " " + str(self.log_type) + " " + str(self.sigid) + " " + str(self.log_version) + " " \
				+ str(self.log_id) + " " + str(self.log_seq_num) + " " + str(self.log_lf)
		return head

	def push_log(self):
		log_output_name = "aie_log.log"
		self.redis_connection.rpush(ReadConfiguration.aie_list_name, self.log)
		output(log_output_name, self.log)

	# def generate_app_log(self):
	# 	app_message_body = "{"
	# 	app_message_body += "\"host\":" + "\"" + self.host + "\","
	# 	app_message_body += "\"method\":" + "\"POST\"," #hard coded
	# 	app_message_body += "\"url\":" + "\"" + self.url + "\","
	# 	app_message_body += "\"t_ra_email\":" + "\"" + self.t_ra_email + "\","
	# 	app_message_body += "\"rsp_code\":" + "\"" + self.rsp_code + "\","
	# 	app_message_body += "\"appname\":" + "\"" + self.appname + "\""
	# 	app_message_body += "}"
	# 	return app_message_body
    #
	# def generate_file_log(self):
	# 	file_message_body = "{"
	# 	file_message_body += "\"host\":" + "\"" + self.host + "\","
	# 	file_message_body += "\"method\":" + "\"GET\", " #hard coded
	# 	file_message_body += "\"url\":" + "\"" + self.url + "\","
	# 	file_message_body += "\"user_agent\":" + "\"" + self.ua + "\","
	# 	file_message_body += "\"rsp_code\":" + "\"" + self.rsp_code + "\","
	# 	file_message_body += "\"rsp_content_type\":" + "\"application/x-msdownload\"," #hard coded
	# 	file_message_body += "\"rsp_latency\":" + str(self.rsp_latency) + ","
	# 	file_message_body += "\"activity\":" + "\"" + self.activity + "\","
	# 	file_message_body += "\"objs\":[{" + "\"type\":" + "\"" + self.obj_type +"\","
	# 	file_message_body += "\"name\":" + "\"" + self.obj_name + "\","
	# 	file_message_body += "\"hash\":" + "\"" + self.obj_hash + "\","
	# 	file_message_body += "\"size\":" + "\"" + str(self.obj_size) + "\""
	# 	file_message_body += "}]"
	# 	file_message_body += "}"
	# 	return file_message_body
    #
	# def generate_login_log(self):
	# 	login_message_body = "{"
	# 	login_message_body += "\"host\":" + "\"" + self.host + "\","
	# 	login_message_body += "\"user_agent\":" + "\"" + self.ua + "\","
	# 	login_message_body += "\"login_name\":" + "\"" + self.login_name + "\","
	# 	login_message_body += "\"rsp_code\":" + "\"" + self.rsp_code +"\","
	# 	login_message_body += "\"success\":" + "true"
	# 	login_message_body += "}"
	# 	return login_message_body




