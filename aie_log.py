import random
import sys
import string
import json
from output import output
from datetime import datetime
from datetime import timedelta
from read_configuration import ReadConfiguration
from read_sql import ReadSQL


class AieLog():
    def __init__(self, redis_connection, table, user):
        self.redis_connection = redis_connection
        self.table = table
        self.user = user
        # timestamp
        self.timestamp = self.generate_timestamp()

    def log_process(self, buffer):
        # gw_id
        gw_id = ReadConfiguration.gw_id
        # aie_id
        aie_id = ReadConfiguration.aie_id
        # mac, src_ip, dst_ip, service got in get_ip_port_session()
        # ip_seg
        ip_seg = self.get_ip_port_session()
        # log_tyep
        log_type = 1  # hard coded
        # log_version
        log_version = 1  # hard coded
        # log_id
        log_id = random.randint(1, 999999)  # arbitrary
        # log_seq_num
        log_seq_num = 0  # hard coded
        # log_lf
        log_lf = 0  # hard coded
        # sig_id
        self.sigid = self.get_sigid()
        # log message head
        message_head = str(self.timestamp) + " " + gw_id + " " + aie_id \
                       + " " + ip_seg + " " + str(log_type) + " " \
                       + self.sigid[1: len(self.sigid) - 1] + " " + str(log_version) + " " \
                       + str(log_id) + " " + str(log_seq_num) + " " + str(log_lf)
        # log message body
        self.message_body_process(buffer)
        # log assemble
        log = message_head + " " + self.message_body
        # push log into redis server
        self.push_log(log)

    def generate_timestamp(self):
        time_show = datetime.now()
        days_delta = -random.randint(0, ReadConfiguration.days)
        hours_delta = -random.randint(0, ReadConfiguration.hours)
        minutes_delta = -random.randint(0, ReadConfiguration.mins)
        seconds_delta = -random.randint(0, 59)
        delta = timedelta(days=days_delta, hours=hours_delta, minutes=minutes_delta, seconds=seconds_delta)
        time_show = time_show + delta
        return time_show.strftime("%Y-%m-%dT%H:%M:%S")

    def get_ip_port_session(self):
        # src
        self.mac = self.table.devices[self.user.device_id]['mac'].encode('utf8')
        self.src_ip = self.table.devices[self.user.device_id]['ip'].encode('utf8')
        self.src_port = random.randint(1, 65535)
        # dst
        if self.user.event is None:
            self.dst_ip = self.table.apps[self.user.appname]['ip'].encode('utf8')
        elif self.user.event == 'download':
            self.dst_ip = self.table.downloads[self.user.appname]['ip'].encode('utf8')
        elif self.user.event == 'upload':
            self.dst_ip = self.table.uploads[self.user.appname]['ip'].encode('utf8')
        else:
            sys.exit("event error!")
        self.dst_port = random.randint(1, 65535)
        self.session_id = random.randint(1, 999999)
        ip_seg = self.src_ip + ":" + str(self.src_port) + ":"
        ip_seg += self.dst_ip + ":" + str(self.dst_port) + ":" + str(self.session_id)
        return ip_seg

    # Should rewrite in file/login log class
    # default 0x7ff0000 is RESTful activity
    def get_sigid(self):
        return "'0x7ff0000'"

    def message_body_process(self, buffer):
        # handle message_body at child class
        # should be rewritten at child class
        body = "{"
        body += "}"
        return body

    def push_log(self, log):
        log_output_name = "aie_log.log"
        self.redis_connection.rpush(ReadConfiguration.aie_list_name, log)
        output(log_output_name, log)

    def generate_body_part(self, buffer):
        context_dict = ReadSQL.get_element_by_sigid(self.sigid, self.table.element_sql.list)
        if self.sigid == "'0x4060000'" or self.sigid == "'0x4050000'":
            context_dict["'http_rsp_downfile_hash'"] = "'file_hash'"
        self.context_dict_process(context_dict, buffer)

    def context_dict_process(self, context_dict, buffer):
        if context_dict is None:
            sys.exit("Something wrong with context_dict_process")
        body = "{"
        objs = ""
        key_list = context_dict.values()
        for context in key_list:
            context = context[1:len(context) - 1]
            if context == 'user_agent':
                self.ua = self.table.devices[self.user.device_id]['ua']
                body += self.string_format(context, self.ua)
                #body += "\"user_agent\":" + "\"" + self.ua.encode('utf8') + "\","
            elif context == 'login_name':
                self.login_name = random.choice(self.table.users[self.user.user_id]['alias'])
                body += self.string_format('login_name', self.login_name)
                #body += "\"login_name\":" + "\"" + self.ua.encode('utf8') + "\","
            elif context == 'user_name@b64':
                self.login_name = random.choice(self.table.users[self.user.user_id]['alias'])
                body += self.string_format('user_name@b64', self.login_name)
            elif context == 'method':
                self.method = random.choice(['GET', 'POST'])
                #body += "\"method\":" + "\"" + self.method + "\","
                body += self.string_format(context, self.method)
            elif context == 'rsp_latency':
                self.rsp_latency = random.randint(1, 100)
                #body += "\"rsp_latency\":" + self.rsp_latency + ","
                body += self.string_format(context, self.rsp_latency)
            elif context == 'file_name':
                if self.table.users[self.user.user_id]['event'][self.user.event]['filename'] == "":
                    self.file_name = self.generate_file_name()
                else:
                    self.file_name = self.table.users[self.user.user_id]['event'][self.user.event]['filename']
                #objs += "\"name\":" + "\"" + self.file_name + "\","
                objs += self.string_format('name', self.file_name)
            elif context == 'file_hash':
                hash = self.get_item_from_buffer('file_hash', buffer)
                if hash == 0:
                    self.file_hash = self.generate_random_hash()
                    buffer['file_hash'] = self.file_hash
                elif hash == -1:
                    self.file_hash = self.generate_random_hash()
                else:
                    self.file_hash = hash
                    buffer.pop('file_hash')
                #objs += "\"hash\":" + "\"" + self.hash + "\","
                objs += self.string_format('hash', self.file_hash)
            elif context == 'file_size':
                size = self.get_item_from_buffer('file_size', buffer)
                if size == 0:
                    self.file_size = random.randint(1000, 99999)
                    buffer['file_size'] = self.file_size
                elif size == -1:
                    self.file_size = random.randint(1000, 99999)
                else:
                    self.file_size = size
                    buffer.pop('file_size')
                #objs += "\"size\":" + self.file_size + ","
                objs += self.string_format('size', self.file_size)
            elif context == 'session_id':
                #objs += "\"session_id\":" + "\"" + str(session_id) + "\","
                objs += self.string_format(context, self.session_id)
            elif context == 'status_code':
                self.rsp_code = self.table.get_item(self.user.event, self.user.appname, 'rsp_code')
                if self.rsp_code is None:
                    sys.exit("rsp_code is None")
                #body += "\"status_code\":" + "\"" + self.rsp_code + "\","
                body += self.string_format(context, self.rsp_code)
            elif context == 'user_id':
                self.user_id = str(random.randint(1, 1000))
                #body += "\"user_id\":" + "\"" + self.user_id + "\","
                body += self.string_format(context, self.user_id)
            elif context == 'user_token':
                # user_token
                self.user_token = 'ABCDEFGHIJKLMNOPQ'
                #body += "\"user_token\":" + "\"" +self.user_token + "\","
                body += self.string_format(context, self.user_token)
            else:
                val = self.table.get_item(self.user.event, self.user.appname, context)
                if val is None:
                    sys.exit("There is no info about context %s" % context)
                if context == 'host':
                    self.host = val
                    #body += "\"host\":" + "\"" +self.host.encode('utf8') + "\","
                    body += self.string_format(context, self.host)
                elif context == 'url':
                    self.url = val
                    #body += "\"url\":" + "\"" + self.url.encode('utf8') + "\","
                    body += self.string_format(context, self.url)
                elif context == 'rsp_code':
                    self.rsp_code = val
                    #body += "\"rsp_code\":" + "\"" + self.rsp_code.encode('utf8') + "\","
                    body += self.string_format(context, self.rsp_code)

        self.message_body = body[0:len(body) - 1]
        self.activity = ReadSQL.get_activity_name(self.sigid, self.table.activity_sql.list)
        if objs != "":
            self.objs = "\"objs\":[{\"type\":\"file\"," + objs[0:len(objs) - 1] + "}]"
            self.message_body += "," + "\"activity\":\"" + self.activity[1 : len(self.activity) - 1] + "\"," + self.objs + "}"
        else:
            self.message_body += "}"
        message_body_json = json.dumps(self.message_body)
        self.message_body = json.loads(message_body_json)

    def generate_random_hash(self, size = 32):
        return ''.join(random.choice(string.ascii_lowercase[0:6] + string.digits) for _ in range(size))

    def generate_file_name(self, size = 8):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    def string_format(self, context, value):
        str = ""
        if context == 'file_size' or context == 'rsp_latency':
            str += "\"%s\":%d," % (context, value)
            return str
        else:
            str += "\"%s\":\"%s\"," % (context, value)
            return str
    def get_item_from_buffer(self, key, buffer):
        if self.table.users[self.user.user_id]['special'] == 'same_file':
            if buffer.has_key(key):
                return buffer[key]
            else:
                return 0
        else:
            return -1