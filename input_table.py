#!/usr/bin/python
# -*- coding:utf-8 -*-


class Input_table:

	def __init__(self, path ,filename):
		self.file = open(path + filename)
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