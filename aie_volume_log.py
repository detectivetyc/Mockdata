#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import random
from output import output
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
		output("aie_volume.log", push_string)
		return

	def random_bytes(self):
		ret_bytes = random.randint(100, 9999)
		return ret_bytes