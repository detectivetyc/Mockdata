#!/usr/bin/python
# -*- coding:utf-8 -*-
import ConfigParser

class ReadConfiguration:

		cf = ConfigParser.ConfigParser()
		cf.read("mock_data.conf")

		redis_host = cf.get("redis", "redis_host")
		redis_port = cf.getint("redis", "redis_port")
		redis_db = cf.getint("redis", "redis_db")
		aie_list_name = cf.get("redis", "aie_list_name")
		gateway_list_name = cf.get("redis", "gateway_list_name")

		mode = cf.get("basic", "mode")
		num = cf.getint("basic", "num")
		req_bytes = cf.getint("basic", "req_bytes")
		rsp_bytes = cf.getint("basic", "rsp_bytes")
		days_delta = cf.getint("basic", "days_delta")
		minutes_delta = cf.getint("basic", "minutes_delta")

		mac_ip_table_name = cf.get("table", "mac_ip_table")
		ip_service_table_name = cf.get("table", "ip_service_table")

		service_appname_table_name = cf.get("app_login_table", "service_appname_table")
		ip_host_table_name = cf.get("app_login_table", "ip_host_table")
		service_url_table_name = cf.get("app_login_table", "service_url_table")
		service_sigid_table_name = cf.get("app_login_table", "service_sigid_table")
		mac_ua_table_name = cf.get("app_login_table", "mac_ua_table")
		service_rspcode_table_name = cf.get("app_login_table", "service_rspcode_table")

		donwload_ip_service_table_name = cf.get("download_table", "download_ip_service_table")
		donwload_service_appname_table_name = cf.get("download_table", "download_service_appname_table")
		donwload_ip_host_table_name = cf.get("download_table", "download_ip_host_table")
		donwload_appname_url_table_name = cf.get("download_table", "download_appname_url_table")
		donwload_appname_rspcode_table_name = cf.get("download_table", "download_appname_rspcode_table")
		donwload_appname_sigid_table_name = cf.get("download_table", "download_appname_sigid_table")