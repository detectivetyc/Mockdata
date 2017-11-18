import random
import sys
from output import output
from datetime import datetime
from datetime import timedelta
from read_configuration import ReadConfiguration


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
        message_body = self.message_body_process(buffer)
        # log assemble
        log = message_head + " " + message_body
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
