#!/usr/bin/python
# -*- coding:utf-8 -*-

import redis

class RedisConnection:

	def __init__(self, port, host, db):
		self.port = port
		self.host = host
		self.db = db
		pool = redis.ConnectionPool(host = self.host, port = self.port, db = self.db)
		self.redis_connection = redis.Redis(connection_pool=pool)