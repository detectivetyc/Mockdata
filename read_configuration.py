#!/usr/bin/python
# -*- coding:utf-8 -*-
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