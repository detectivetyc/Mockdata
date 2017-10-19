from input_table import Input_table
from read_configuration import ReadConfiguration

class ReadFile:
    table_path = "MockDataInput/"
    app_table_list = {}
    file_table_list = {}

    mac_ip_table = Input_table(table_path, ReadConfiguration.mac_ip_table_name)
    mac_ua_table = Input_table(table_path, ReadConfiguration.mac_ua_table_name)

    file_table_path = table_path + "file/"
    file_ip_service_table = Input_table(file_table_path, ReadConfiguration.donwload_ip_service_table_name)
    file_service_appname_table = Input_table(file_table_path, ReadConfiguration.donwload_service_appname_table_name)
    file_ip_host_table = Input_table(file_table_path, ReadConfiguration.donwload_ip_host_table_name)
    file_appname_url_table = Input_table(file_table_path, ReadConfiguration.donwload_appname_url_table_name)
    file_appname_rspcode_table = Input_table(file_table_path, ReadConfiguration.donwload_appname_rspcode_table_name)
    file_appname_sigid_table = Input_table(file_table_path, ReadConfiguration.donwload_appname_sigid_table_name)
    # file_table_list["download-ip-service"] = download_ip_service_table
    # file_table_list["download-service-appname"] = download_service_appname_table
    # file_table_list["download-ip-host"] = download_ip_host_table
    # file_table_list["download-appname-url"] = download_appname_url_table
    # file_table_list["download-appname-rspcode"] = download_appname_rspcode_table
    # file_table_list["download-appname-sigid"] = download_appname_sigid_table

    app_login_table_path = table_path + "app_login/"
    app_service_appname_table = Input_table(app_login_table_path, ReadConfiguration.service_appname_table_name)
    app_ip_service_table = Input_table(app_login_table_path, ReadConfiguration.ip_service_table_name)
    app_ip_host_table = Input_table(app_login_table_path, ReadConfiguration.ip_host_table_name)
    app_service_url_table = Input_table(app_login_table_path, ReadConfiguration.service_url_table_name)
    app_service_rspcode_table = Input_table(app_login_table_path, ReadConfiguration.service_rspcode_table_name)
    app_service_sigid_table = Input_table(app_login_table_path, ReadConfiguration.service_sigid_table_name)
    # app_table_list["ip-service"] = ip_service_table
    # app_table_list["service-appname"] = service_appname_table
    # app_table_list["ip-host"] = ip_host_table
    # app_table_list["service-url"] = service_url_table
    # app_table_list["service-rspcode"] = service_rspcode_table
    # app_table_list["service-sigid"] = service_sigid_table