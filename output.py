#!/usr/bin/python
# -*- coding:utf-8 -*-


def output(log_output_name, output_string, log_output_path = "/Users/yuchentang/Documents/pythonDoc/output/"):
	output_file = open(log_output_path + log_output_name, "a")
	output_file.write(output_string)
	output_file.write("\n")
	output_file.close()
