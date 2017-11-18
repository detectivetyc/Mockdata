import sys
import random

class ReadSQL:

    def __init__(self, path, filename):
        self.file = open(path + filename)
        self.list = []
        self.read_sql_file()

    def read_sql_file(self):
        for line in self.file.readlines():
            if len(line) <= 1:
                continue
            line = line.strip('\n').split('||')
            if line[0][0] == "T":
                line[0] = line[0][3:]
                for i in range(len(line)):
                    line[i] = line[i].strip(' ')
                self.list.append(line)
    @classmethod
    def find_by_appname(cls, appname, list):
        appname = "'" + appname + "'"
        list_by_appname = []
        for i in range(len(list)):
            if list[i][2] == appname:
                list_by_appname.append(list[i])
        if len(list_by_appname) == 0:
            sys.exit("No such appname")
        return list_by_appname
    @classmethod
    def find_by_sigid(cls, sigid, list):
        list_by_sigid = []
        for i in range(len(list)):
            if list[i][0] == sigid:
                list_by_sigid.append(list[i])
        if len(list_by_sigid) == 0:
            sys.exit("No such sigid")
        return list_by_sigid
    @classmethod
    def find_by_name(cls, name, list, appname):
        list_by_name = []
        name = "'" + name + "'"
        for i in range(len(list)):
            if list[i][1] == name:
                list_by_name.append(list[i])
        if len(list_by_name) == 0:
            sys.exit("No such name")
        return list_by_name
    @classmethod
    def get_event_sigid_from_sql(cls, appname, list, event):
        list_by_appname = cls.find_by_appname(appname, list)
        if len(list_by_appname) > 1:
            list_tmp = cls.find_by_name(event, list_by_appname, appname)
            if len(list_tmp) > 1:
                list_tmp.sort()
                for i in range(len(list_tmp)):
                    if len(list_tmp[i]) > 5 and list_tmp[i][5] == "\'\"success\":true\'":
                        return list_tmp[i][0]
                    else:
                        return list_tmp[0][0]
            else:
                return list_tmp[0][0]
        else:
            return list_by_appname[0][0]
    @classmethod
    def get_element_by_sigid(cls, sigid, element_list):
        list_by_sigid = ReadSQL.find_by_sigid(sigid, element_list)
        context_dict = {}
        for i in range(len(list_by_sigid)):
            if list_by_sigid[i][0] == sigid:
                if list_by_sigid[i][2] == "'log'" and list_by_sigid[i][3] != "''":
                    context_dict[list_by_sigid[i][1]] = list_by_sigid[i][3]
        if len(context_dict) == 0:
            sys.exit("no such sigid")
        return context_dict
    @classmethod
    def get_activity_name(cls, sigid, activity_list):
        list_by_sigid = ReadSQL.find_by_sigid(sigid, activity_list)
        if len(list_by_sigid) > 0 :
            if list_by_sigid[0][1] != "''":
                return list_by_sigid[0][1]