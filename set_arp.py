#!/usr/bin/python
# -*- coding:utf-8 -*-

class Set_arp:

	def __init__(self, mac_ip_table, redis_connection):
		self.mac_ip_table = mac_ip_table
		self.redis_connection = redis_connection 
		self.gw_id = "G011609F3C98"
		self.set_arp_table()

	def set_arp_table(self):
		arp_seg_head = "arp#" + self.gw_id + "#"
		for key, value in self.mac_ip_table.dict.iteritems():
			redis_key = arp_seg_head + str(self.mac_ip_table.dict[key])
			redis_string = str(key)
			self.redis_connection.set(redis_key, redis_string)
			#self.redis_connection.expire(redis_key, 90)