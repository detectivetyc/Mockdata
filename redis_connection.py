#!/usr/bin/python
# -*- coding:utf-8 -*-

import redis

class Redis_Connection:

	def __init__(self, port, host, db):
		self.port = port
		self.host = host
		self.db = db
		self.redis_connection = self.redis_connect()

	def redis_connect(self):
		r = redis.Redis(host = self.host, port = self.port, db = self.db)
		return r