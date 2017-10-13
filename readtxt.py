#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import random
import sys
import redis
import ConfigParser


class Read_Configuration:

	def __init__(self, path, filename):
		self.cf = ConfigParser.ConfigParser()
		self.path = path
		self.filename = filename
		self.read_Redis()
		self.read_Basic()
		self.read_Table()

	def read_Redis(self):
		self.cf.read(self.path + self.filename)
		self.redis_host = self.cf.get("redis", "redis_host")
		self.redis_port = self.cf.getint("redis", "redis_port")
		self.redis_db = self.cf.getint("redis", "redis_db")
		self.aie_list_name = self.cf.get("redis", "aie_list_name")
		self.gateway_list_name = self.cf.get("redis", "gateway_list_name")

	def read_Basic(self):
		self.cf.read(self.path + self.filename)
		self.mode = self.cf.get("basic", "mode")
		self.num = self.cf.getint("basic", "num")
		self.req_bytes = self.cf.getint("basic", "req_bytes")
		self.rsp_bytes = self.cf.getint("basic", "rsp_bytes")

	def read_Table(self):
		self.cf.read(self.path + self.filename)
		self.mac_ip_table_name = self.cf.get("table", "mac_ip_table")
		self.ip_service_table_name = self.cf.get("table", "ip_service_table")
		self.service_sigid_table_name = self.cf.get("table", "service_sigid_table")
		self.ip_host_table_name = self.cf.get("table", "ip_host_table")
		self.service_url_table_name = self.cf.get("table", "service_url_table")
		self.sigid_appname_table_name = self.cf.get("table", "sigid_appname_table")
		self.mac_ua_table_name = self.cf.get("table", "mac_ua_table")
		self.service_rspcode_table_name = self.cf.get("table", "service_rspcode_table")


class Redis_Connection:

	def __init__(self, port, host, db):
		self.port = port
		self.host = host
		self.db = db
		self.redis_connection = self.redis_connect()

	def redis_connect(self):
		r = redis.Redis(host = self.host, port = self.port, db = self.db)
		return r


class Set_arp:

	def __init__(self, mac_ip_table, redis_connection):
		self.mac_ip_table = mac_ip_table
		self.redis_connection = redis_connection 
		self.gw_id = "G011609F3C98"
		self.set_arp_table()

	def set_arp_table(self):
		arp_seg_head = "arp#" + self.gw_id + "#"
		print "arp table: "
		for key, value in self.mac_ip_table.dict.iteritems():
			redis_key = arp_seg_head + str(self.mac_ip_table.dict[key])
			redis_string = str(key)
			self.redis_connection.set(redis_key, redis_string)
			print redis_key, redis_string
			#self.redis_connection.expire(redis_key, 90)

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


class Aie_volume_log:

	def __init__(self, aie_log):
		self.aie_log = aie_log

	def log_init(self):
		#timestamp
		self.timestamp = self.aie_log.timestamp
		#aie_id
		self.aie_id = "HOLOFLOW_IN_TEST"
		#request src_ip
		self.req_src = self.aie_log.src_ip
		#request port
		self.req_spt = self.aie_log.src_port
		#response ip
		self.req_dst = self.aie_log.dst_ip
		#response port
		self.req_dpt = self.aie_log.dst_port
		#request protocol
		self.req_proto = "tcp"
		#request volume
		#read configuration file
		#self.req_bytes = self.read_conf.req_bytes
		#random bytes
		self.req_bytes = self.random_bytes()
		#response volume
		#read configuration file
		#self.rsp_bytes = self.read_conf.rsp_bytes
		#random bytes
		self.rsp_bytes = self.random_bytes()
		#app layer protocol
		self.app_proto = "HTTP"
		#ssl
		self.ssl = "true"
		#duration
		self.duration = 1
		#request hf latency
		self.req_hf_latency = 1
		#response hf latency
		self.rsp_hf_latency = 1
		#request ssl latency
		self.req_ssl_latency = 1
		#request domain
		self.req_dn = self.aie_log.host
		#domain acc
		self.dn_acc = "true"
		#appname
		self.appname = self.aie_log.appname
		#gw_id
		self.gw_id = self.aie_log.gw_id

		self.push_log()

	def push_log(self):
		push_string = "{"
		push_string += "\"timestamp\":" + "\"" + str(self.timestamp) + "\","
		push_string += "\"aie_id\":" + "\"" + self.aie_id + "\","
		push_string += "\"req_src\":" + "\"" + self.req_src + "\","
		push_string += "\"req_spt\":" + str(self.req_spt) + ","
		push_string += "\"req_dst\":" + "\"" + self.req_dst + "\","
		push_string += "\"req_dpt\":" + str(self.req_dpt) + ","
		push_string += "\"req_proto\":" + "\"" + self.req_proto + "\","
		push_string += "\"req_bytes\":" + str(self.req_bytes) + ","
		push_string += "\"rsp_bytes\":" + str(self.rsp_bytes) + ","
		push_string += "\"app_proto\":" + "\"" + self.app_proto + "\","
		push_string += "\"ssl\":" + self.ssl + ","
		push_string += "\"duration\":" + str(self.duration) + ","
		push_string += "\"req_hf_latency\":" + str(self.req_hf_latency) + ","
		push_string += "\"rsp_hf_latency\":" + str(self.rsp_hf_latency) + ","
		push_string += "\"req_ssl_latency\":" + str(self.req_ssl_latency) + ","
		push_string += "\"req_dn\":" + "\"" + self.req_dn + "\","
		push_string += "\"dn_acc\":" + self.dn_acc + ","
		push_string += "\"appname\":" + "\"" + self.appname + "\","
		push_string += "\"gw_id\":" + "\"" + self.gw_id + "\""
		push_string += "}"

		self.aie_log.redis_connection.rpush(self.aie_log.read_conf.gateway_list_name, push_string)
		print "aie_volume: "
		print push_string
		return

	def random_bytes(self):
		ret_bytes = random.randint(100, 9999)
		return ret_bytes


class Input_table:

	def __init__(self, path ,filename):
		self.file = open(path + "/" + filename)
		self.dict = {}
		self.keys = []
		self.values = []
		self.read_file()

	def read_file(self):
		while 1:
			line = self.file.readline()
			if not line:
				break
			line = line.strip('\n').split(" ", 1)
			self.dict[line[0]] = line[1]
			self.keys.append(line[0])
			self.values.append(line[1])
		self.file.close()
		return

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