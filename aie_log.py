#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import random
import string
import sys
from output import output
from datetime import datetime
from datetime import timedelta
from read_configuration import ReadConfiguration


class AieLog(ReadConfiguration):
	def __init__(self, redis_connection, table_list):
		self.redis_connection = redis_connection
		self.table_list = table_list
	def log_init(self):
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
		# t_ra_email (hard coded)
		self.t_ra_email = "tony@holonetsecurity.com"
		# rsp_latency
		self.rsp_latency = 101
		# appname
		self.appname = self.get_appname()
		# download-sigid
		self.sigid = self.get_sigid()
		# download-host
		self.host = self.get_host()
		# activity
		self.activity = "download"
		# url
		self.url = self.get_url()
		# rsp_code
		self.rsp_code = self.get_rspcode()
		# file objects
		# type
		self.obj_type = "file"
		# obj_name
		self.obj_name = self.generate_random_name(8) + '.doc'
		# obj_hash
		self.obj_hash = self.generate_random_hash()
		# obj_size
		self.obj_size = random.randint(2000, 99999)
		# file message body
		self.file_message_body = self.generate_file_log()
		# login_name
		self.login_name = self.get_login_name()
	def generate_timestamp(self):
		pass
	def get_ip_port_session(self):
		pass
	def get_ua(self):
		pass
	def get_appname(self):
		pass
	def get_sigid(self):
		pass
	def get_host(self):
		pass
	def get_url(self):
		pass
	def get_rspcode(self):
		pass
	def generate_random_name(self, size):
		pass
	def generate_random_hash(self, size = 32):
		pass
	def generate_file_log(self):
		pass
	def get_login_name(self):
		pass
class Aie_log:

	def __init__(self, mode, redis_connection, table_list):
		self.mode = mode
		self.redis_connection = redis_connection
		self.table_list = table_list
		
	def log_init(self):
		ret = 0
		#timestamp
		self.timestamp = self.generate_timestamp()
		#gw_id
		self.gw_id = "G011609F3C98"
		#aie_id
		self.aie_id = "HOLOFLOW_IN_TEST"
		#mac, src_ip, dst_ip, service got in get_ip_port_session()
		#ip_seg
		self.ip_seg = self.get_ip_port_session()
		#log_tyep
		self.log_type = 1
		#log_version
		self.log_version = 1
		#log_id
		self.log_id = random.randint(1, 999999)
		#log_seq_num
		self.log_seq_num = 0
		#log_lf
		self.log_lf = 0
		#user agent
		self.ua = self.get_ua()
		#method
		self.method = ["POST", "PUT", "GET", "CONNECT", "HEAD", "OPTIONS", "TRACE"] #hard coded
		#t_ra_email (hard coded)
		self.t_ra_email = "tony@holonetsecurity.com"
		#rsp_latency
		self.rsp_latency = 101
		if self.mode == "file":
			#appname
			self.appname = self.get_download_appname()
			#download-sigid
			self.sigid = self.get_download_sigid()
			#download-host
			self.host = self.get_download_host()
			#activity
			self.activity = "download"
			#url
			self.url = self.get_download_url()
			#rsp_code
			self.rsp_code = self.get_download_rspcode()
			#file objects
			#type
			self.obj_type = "file"
			#obj_name
			self.obj_name = self.generate_random_name(8) + '.doc'
			#obj_hash
			self.obj_hash = self.generate_random_hash()
			#obj_size
			self.obj_size = random.randint(2000,99999)
			#file message body
			self.file_message_body = self.generate_file_log()
			ret = self.push_log()
			return ret

		else:
			#appname
			self.appname = self.get_appname()
			#sigid
			self.sigid = self.get_sigid()
			#host
			self.host = self.get_host()
			#url
			self.url = self.get_url()
			#rsp_code
			self.rsp_code = self.get_rspcode()
			#login_name
			self.login_name = "tony@holonetsecurity.com"   #can be configured by configuration file
			if self.mode == "app":
				self.app_message_body = self.generate_app_log()
				ret = self.push_log()
				return ret
			if self.mode == "login":
				self.login_message_body = self.generate_login_log()
				ret = self.push_log()
				return ret		
			else:
				sys.exit("Wrong mode in Conf file!")		

	def generate_random_name(self, size):
		return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

	def generate_random_hash(self, size = 32):
		return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))

	def generate_app_log(self):
		app_message_body = "{"
		app_message_body += "\"host\":" + "\"" + self.host + "\","
		app_message_body += "\"method\":" + "\"POST\"," #hard coded
		app_message_body += "\"url\":" + "\"" + self.url + "\"," 
		app_message_body += "\"t_ra_email\":" + "\"" + self.t_ra_email + "\","
		app_message_body += "\"rsp_code\":" + "\"" + self.rsp_code + "\","
		app_message_body += "\"appname\":" + "\"" + self.appname + "\""
		app_message_body += "}"
		return app_message_body

	def generate_file_log(self):
		file_message_body = "{"
		file_message_body += "\"host\":" + "\"" + self.host + "\","
		file_message_body += "\"method\":" + "\"GET\", " #hard coded
		file_message_body += "\"url\":" + "\"" + self.url + "\","
		file_message_body += "\"user_agent\":" + "\"" + self.ua + "\","
		file_message_body += "\"rsp_code\":" + "\"" + self.rsp_code + "\","
		file_message_body += "\"rsp_content_type\":" + "\"application/x-msdownload\"," #hard coded
		file_message_body += "\"rsp_latency\":" + str(self.rsp_latency) + ","
		file_message_body += "\"activity\":" + "\"" + self.activity + "\","
		file_message_body += "\"objs\":[{" + "\"type\":" + "\"" + self.obj_type +"\","
		file_message_body += "\"name\":" + "\"" + self.obj_name + "\","
		file_message_body += "\"hash\":" + "\"" + self.obj_hash + "\","
		file_message_body += "\"size\":" + "\"" + str(self.obj_size) + "\""
		file_message_body += "}]"
		file_message_body += "}"
		return file_message_body

	def generate_login_log(self):
		login_message_body = "{"
		login_message_body += "\"host\":" + "\"" + self.host + "\","
		login_message_body += "\"user_agent\":" + "\"" + self.ua + "\","
		login_message_body += "\"login_name\":" + "\"" + self.login_name + "\","
		login_message_body += "\"rsp_code\":" + "\"" + self.rsp_code +"\","
		login_message_body += "\"success\":" + "true"
		login_message_body += "}"
		return login_message_body

	def generate_timestamp(self):
		time_show = datetime.now()
		delta = timedelta(days = self.days_delta, minutes = self.read_conf.minutes_delta)
		time_show = time_show + delta
		return time_show.strftime("%Y-%m-%dT%H:%M:%S")

	def get_ip_port_session(self):
		#src
		self.mac_ip_table = self.table_list["mac-ip"]
		self.mac = random.choice(self.mac_ip_table.keys)
		self.src_ip = self.mac_ip_table.dict[self.mac]
		self.src_port = random.randint(1, 65535)
		#dst
		if self.mode == "file":
			self.download_ip_service_table = self.table_list["download-ip-service"]
			self.dst_ip = random.choice(self.download_ip_service_table.keys)
			self.service = self.download_ip_service_table.dict[self.dst_ip]
		else:
			self.ip_service_table = self.table_list["ip-service"]
			self.dst_ip = random.choice(self.ip_service_table.keys)
			self.service = self.ip_service_table.dict[self.dst_ip]
		self.dst_port = random.randint(1, 65535)
		self.session_id = random.randint(1, 999999)
		ip_seg = self.src_ip + ":" +str(self.src_port) + ":"
		ip_seg += self.dst_ip + ":" + str(self.dst_port) + ":" + str(self.session_id)
		return ip_seg

	def get_download_sigid(self):
		self.download_appname_sigid_table = self.table_list["download-appname-sigid"]
		return self.download_appname_sigid_table.dict[self.appname]

	def get_sigid(self):
		self.service_sigid_table = self.table_list["service-sigid"]
		return self.service_sigid_table.dict[self.service]

	def get_download_host(self):
		self.download_ip_host_table = self.table_list["download-ip-host"]
		return self.download_ip_host_table.dict[self.dst_ip]

	def get_host(self):
		self.ip_host_table = self.table_list["ip-host"]
		return self.ip_host_table.dict[self.dst_ip]

	def get_download_url(self):
		self.download_appname_url_table = self.table_list["download-appname-url"]
		return self.download_appname_url_table.dict[self.appname]

	def get_url(self):
		self.service_url_table = self.table_list["service-url"]
		return self.service_url_table.dict[self.service]

	def get_download_rspcode(self):
		self.download_appname_rspcode_table = self.table_list["download-appname-rspcode"]
		return self.download_appname_rspcode_table.dict[self.appname]

	def get_rspcode(self):
		self.service_rspcode_table = self.table_list["service-rspcode"]
		return self.service_rspcode_table.dict[self.service]

	def get_download_appname(self):
		self.download_service_appname_table = self.table_list["download-service-appname"]
		return self.download_service_appname_table.dict[self.service]

	def get_appname(self):
		self.service_appname_table = self.table_list["service-appname"]
		return self.service_appname_table.dict[self.service]

	def get_ua(self):
		self.mac_ua_table = self.table_list["mac-ua"]
		return self.mac_ua_table.dict[self.mac]

	def push_log(self):
		log_output_name = "aie_log.log"
		string_head = str(self.timestamp) + " " + self.gw_id + " " + str(self.aie_id) + " " + str(self.ip_seg) \
					+ " " + str(self.log_type) + " " + str(self.sigid) + " " + str(self.log_version) + " " \
					+ str(self.log_id) + " " + str(self.log_seq_num) + " " + str(self.log_lf)
		if self.mode == "app":
			app_log = string_head + " " + self.app_message_body
			self.redis_connection.rpush(self.read_conf.aie_list_name, app_log)
			output(log_output_name, app_log)
			#print self.app_message_body
			return 1
		elif self.mode == "file":
			file_log = string_head + " " + self.file_message_body 
			self.redis_connection.rpush(self.read_conf.aie_list_name, file_log)
			output(log_output_name, file_log)
			#print self.file_message_body
			return 1
		elif self.mode == "login":
			login_log = string_head + " " + self.login_message_body
			self.redis_connection.rpush(self.read_conf.aie_list_name, login_log)
			output(log_output_name, login_log)
			#print self.login_message_body
			return 1
		else:
			return -1


