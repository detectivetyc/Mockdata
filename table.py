from read_sql import ReadSQL
from read_configuration import ReadConfiguration
import json
import random
import sys

class Table:

    def __init__(self, table_path = "MockDataInput/"):
        #get sql tables
        sql_table_path = table_path + "SQL/"
        self.activity_sql = ReadSQL(sql_table_path, ReadConfiguration.activity_sql_name)
        self.context_sql = ReadSQL(sql_table_path, ReadConfiguration.context_sql_name)
        self.element_sql = ReadSQL(sql_table_path, ReadConfiguration.element_sql_name)
        self.service_sql = ReadSQL(sql_table_path, ReadConfiguration.service_sql_name)
        #get users table
        self.users = self.load_json_file(ReadConfiguration.user_table_path, ReadConfiguration.user_table_name)
        #get devices table
        self.devices = self.load_json_file(ReadConfiguration.device_table_path, ReadConfiguration.device_table_name)
        #get app table
        self.apps = self.load_json_file(ReadConfiguration.app_table_path, ReadConfiguration.app_table_name)
        #get content scan pattern
        self.patterns = self.load_json_file(table_path, 'pattern.json')
        self.get_items_from_pattern_json()
        #generate list from User Table:
        self.user_list = []
        if isinstance(self.users, dict):
            for key in self.users:
                self.user_list.append(key)
        self.user_list.sort()
        self.mac_ip_dict = self.generate_mac_ip_table()
        #generate app list
        self.app_list = []
        if isinstance(self.apps, dict):
            for key in self.apps:
                self.app_list.append(key)
        #download
        self.downloads = self.load_json_file(ReadConfiguration.download_table_path, ReadConfiguration.download_table_name)
        #upload
        self.uploads = self.load_json_file(ReadConfiguration.upload_table_path, ReadConfiguration.upload_table_name)

    def load_json_file(self, path, name):
        table_path = path + name
        table_file = open(table_path)
        table_content = json.load(table_file)
        table_file.close()
        return table_content

    def randomly_get_device_id(self, user_id):
        return random.choice(self.users[user_id]['devices'])

    def randomly_get_app_name(self, user_id):
        if self.users[user_id]['apps'][0] == 'all':
            return random.choice(self.app_list)
        else:
            return random.choice(self.users[user_id]['apps'])

    def randomly_get_file_item(self, user_id, event, item_name):
        if event is None:
            return None
        elif event == 'download':
            return random.choice(self.users[user_id]['event']['download'][item_name])
        elif event == 'upload':
            return random.choice(self.users[user_id]['event']['upload'][item_name])
        else:
            sys.exit('No such event!')

    def generate_mac_ip_table(self):
        mac_list = []
        ip_list = []
        if isinstance(self.devices, dict):
            for key in self.devices:
                mac_list.append(self.devices[key]['mac'])
                ip_list.append(self.devices[key]['ip'])
        return dict(zip(mac_list, ip_list))

        #print Table.mac_ip_dict

    def get_item(self, event, appname, item_name):
        if event is None and self.apps[appname].has_key(item_name):
            return self.apps[appname][item_name]
        elif event == 'download' and self.downloads[appname].has_key(item_name):
            return self.downloads[appname][item_name]
        elif event == 'upload' and self.uploads[appname].has_key(item_name):
            return self.uploads[appname][item_name]
        else:
            return None
    def get_items_from_pattern_json(self):
        self.name_list = []
        self.name_group_dict = {}
        group_list = []
        pattern_list = self.patterns['content_scan']
        for item in pattern_list:
            self.name_list.append(item['name'])
            self.name_group_dict[item['name']] = item['group']
            group_list.append(item['group'])
        self.group_set = set(group_list)
