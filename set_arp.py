#!/usr/bin/python
# -*- coding:utf-8 -*-
from read_configuration import ReadConfiguration

class SetArp:

	def __init__(self, redis_connection, table):
		self.mac_ip_table = table.mac_ip_dict
		self.redis_connection = redis_connection 
		self.gw_id = ReadConfiguration.gw_id
		self.set_arp_table()

	def set_arp_table(self):
		arp_seg_head = "arp#" + self.gw_id + "#"
		for key, value in self.mac_ip_table.iteritems():
			redis_key = arp_seg_head + str(self.mac_ip_table[key])
			redis_string = str(key)
			self.redis_connection.set(redis_key, redis_string)
			#print key, value
			#self.redis_connection.expire(redis_key, 90)