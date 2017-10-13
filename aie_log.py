#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import random

class Aie_log:

	def __init__(self, mode, redis_connection, read_conf, path, table_list):
		self.path = path
		self.mode = mode
		self.redis_connection = redis_connection
		self.read_conf = read_conf
		self.table_list = table_list
		
	def log_init(self):
		ret = 0
		#timestamp
		self.timestamp = self.generate_timestamp()
		#gw_id
		self.gw_id = "G011609F3C98"
		#aie_id
		self.aie_id = "HOLOFLOW_IN_TEST"
		#ip_seg
		self.ip_seg = self.get_ip_port_session()
		#log_tyep
		self.log_type = 1
		#sigid
		self.sigid = self.get_sigid()
		#log_version
		self.log_version = 1
		#log_id
		self.log_id = random.randint(1, 999999)
		#log_seq_num
		self.log_seq_num = 0
		#log_lf
		self.log_lf = 0
		#host
		self.host = self.get_host()
		#method
		self.method = ["POST", "PUT", "GET", "CONNECT", "HEAD", "OPTIONS", "TRACE"]
		#url
		self.url = self.get_url()
		#t_ra_email (hard coded)
		self.t_ra_email = "tony@holonetsecurity.com"
		#rsp_code
		self.rsp_code = self.get_rspcode()
		#appname
		self.appname = self.get_appname()
		#mac, src_ip, dst_ip, service got in get_ip_port_session()
		#user agent
		self.ua = self.get_ua()
		#rsp_latency
		self.rsp_latency = 101
		#activity
		self.activity = "download"
		#file objects
		#type
		self.obj_type = "file"
		self.obj_name = "123.exe"
		self.obj_hash = "4571653d8e2dbd19ea9b9ff20b3d3873"
		self.obj_size = random.randint(1000,99999)
		#login_name
		self.login_name = "tony@holonetsecurity.com"

		if self.mode == "app":
			self.app_message_body = self.generate_app_log()
			ret = self.push_log()
			return ret
		elif self.mode == "file":
			self.file_message_body = self.generate_file_log()
			ret = self.push_log()
			return ret
		elif self.mode == "login":
			self.login_message_body = self.generate_login_log()
			ret = self.push_log()
			return ret
		else:
			sys.exit("Wrong mode in Conf file!")		

	def generate_app_log(self):
		app_message_body = "{"
		app_message_body += "\"host\":" + "\"" + self.host + "\","
		app_message_body += "\"method\":" + "\"POST\"," # hard code 
		app_message_body += "\"url\":" + "\"" + self.url + "\"," 
		app_message_body += "\"t_ra_email\":" + "\"" + self.t_ra_email + "\","
		app_message_body += "\"rsp_code\":" + "\"" + self.rsp_code + "\","
		app_message_body += "\"appname\":" + "\"" + self.appname + "\""
		app_message_body += "}"
		return app_message_body

	def generate_file_log(self):
		file_message_body = "{"
		file_message_body += "\"host\":" + "\"" + self.host + "\","
		file_message_body += "\"method\":" + "\"GET\", " # hard code
		file_message_body += "\"url\":" + "\"" + self.url + "\","
		file_message_body += "\"user_agent\":" + "\"" + self.ua + "\","
		file_message_body += "\"rsp_code\":" + "\"" + self.rsp_code + "\","
		file_message_body += "\"rsp_content_type\":" + "\"application/x-msdownload\"," #hard code
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
		return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()))

	def get_ip_port_session(self):
		self.mac_ip_table = self.table_list["mac-ip"]
		self.mac = random.choice(self.mac_ip_table.keys)
		self.src_ip = self.mac_ip_table.dict[self.mac]
		self.src_port = random.randint(1, 65535)
		self.ip_service_table = self.table_list["ip-service"]
		self.dst_ip = random.choice(self.ip_service_table.keys)
		self.dst_port = random.randint(1, 65535)
		self.service = self.ip_service_table.dict[self.dst_ip]
		ip_seg = self.src_ip + ":" +str(self.src_port) + ":"
		ip_seg += self.dst_ip + ":" + str(self.dst_port) + ":" + str(random.randint(1,999999))
		return ip_seg

	def get_sigid(self):
		self.service_sigid_table = self.table_list["service-sigid"]
		self.ip_service_table = self.table_list["ip-service"]
		self.service = self.ip_service_table.dict[self.dst_ip]
		return self.service_sigid_table.dict[self.service]

	def get_host(self):
		self.ip_host_table = self.table_list["ip-host"]
		return self.ip_host_table.dict[self.dst_ip]

	def get_url(self):
		self.service_url_table = self.table_list["service-url"]
		return self.service_url_table.dict[self.service]

	def get_rspcode(self):
		self.service_rspcode_table = self.table_list["service-rspcode"]
		return self.service_rspcode_table.dict[self.service]

	def get_appname(self):
		self.sigid_appname_table = self.table_list["sigid-appname"]
		return self.sigid_appname_table.dict[self.sigid]

	def get_ua(self):
		self.mac_ua_table = self.table_list["mac-ua"]
		return self.mac_ua_table.dict[self.mac]

	def push_log(self):
		string_head = str(self.timestamp) + " " + self.gw_id + " " + str(self.aie_id) + " " + str(self.ip_seg) \
					+ " " + str(self.log_type) + " " + str(self.sigid) + " " + str(self.log_version) + " " \
					+ str(self.log_id) + " " + str(self.log_seq_num) + " " + str(self.log_lf)
		if self.mode == "app":
			app_log = string_head + " " + self.app_message_body
			self.redis_connection.rpush(self.read_conf.aie_list_name, app_log)
			print "aie: "
			print app_log
			#print self.app_message_body
			return 1
		elif self.mode == "file":
			file_log = string_head + " " + self.file_message_body 
			self.redis_connection.rpush(self.read_conf.aie_list_name, file_log)
			print "aie: "
			print file_log
			#print self.file_message_body
			return 1
		elif self.mode == "login":
			login_log = string_head + " " + self.login_message_body
			self.redis_connection.rpush(self.read_conf.aie_list_name, login_log)
			print "aie: "
			print login_log
			#print self.login_message_body
			return 1
		else:
			return -1


