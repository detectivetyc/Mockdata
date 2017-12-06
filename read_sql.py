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

    #index_id
    #sigid - 0
    #name - 1
    #appname - 2
    @classmethod
    def find_item_by_index(cls, index, index_id, list):
        index = "'" + index + "'"
        ret_list = []
        for i in range(len(list)):
            if list[i][index_id] == index:
                ret_list.append(list[i])
        if len(ret_list) == 0:
            sys.exit("Cannot find item %s" % (index))
        return ret_list

    @classmethod
    def get_event_sigid_from_sql(cls, appname, list, event):
        list_by_appname = cls.find_item_by_index(appname, 2, list)
        if len(list_by_appname) > 1:
            list_tmp = cls.find_item_by_index(event, 1, list_by_appname)
            if len(list_tmp) > 1:
                list_tmp.sort()
                for i in range(len(list_tmp)):
                    if len(list_tmp[i]) > 5 and list_tmp[i][5] == "\'\"success\":true\'":
                        return list_tmp[i][0]
                    else:
                        continue
                        #return list_tmp[0][0]
                return list_tmp[0][0]
            else:
                return list_tmp[0][0]
        else:
            return list_by_appname[0][0]

    @classmethod
    def get_element_by_sigid(cls, sigid, element_list):
        if sigid is None or element_list is None:
            sys.exit("Something wrong with get_element_by_sigid")
        list_by_sigid = cls.find_item_by_index(sigid, 0, element_list)
        context_dict = {}
        for i in range(len(list_by_sigid)):
            if list_by_sigid[i][0] == "'" + sigid + "'":
                if list_by_sigid[i][2] == "'log'" and list_by_sigid[i][3] != "''":
                    context_dict[list_by_sigid[i][1]] = list_by_sigid[i][3]
        if len(context_dict) == 0:
            sys.exit("no such sigid")
        return context_dict

    @classmethod
    def get_activity_name(cls, sigid, activity_list):
        list_by_sigid = ReadSQL.find_item_by_index(sigid, 0, activity_list)
        if len(list_by_sigid) > 0 :
            if list_by_sigid[0][1] != "''":
                return list_by_sigid[0][1]