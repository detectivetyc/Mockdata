from aie_log import AieLog
from read_configuration import ReadConfiguration
from output import output
from read_file import ReadFile
import random
import string

class FileLog(AieLog):

    def message_body_process(self):
        # host got from AieLog::log_process
        # method
        self.method = "GET"
        # url got from AieLog::log_process
        # ua got from AieLog::log_process
        # rsp_code got from AieLog::log_process
        # rsp_content_type
        self.rsp_content_type = "application/x-msdownload"
        # rsp_latency
        self.rsp_latency = "1"
        # activity
        self.activity = "download"
        # obj_type
        self.obj_type = "file"
        # file name
        self.obj_name = self.generate_random_name(8) + '.doc'
        # obj hash
        self.obj_hash = self.generate_random_hash()
        # obj size
        self.obj_size = random.randint(2000, 99999)

        message_body = "{"
        message_body += "\"host\":" + "\"" + self.host + "\","
        message_body += "\"method\":" + "\""+ self.method + "\"," #hard coded
        message_body += "\"url\":" + "\"" + self.url + "\","
        message_body += "\"user_agent\":" + "\"" + self.ua + "\","
        message_body += "\"rsp_code\":" + "\"" + self.rsp_code + "\","
        message_body += "\"rsp_content_type\":" + "\"" + self.rsp_content_type + "\"," #hard coded
        message_body += "\"rsp_latency\":" + self.rsp_latency + ","
        message_body += "\"activity\":" + "\"" + self.activity + "\"," #hard coded
        message_body += "\"objs\":[{" + "\"type\":" + "\"" + self.obj_type +"\","
        message_body += "\"name\":" + "\"" + self.obj_name + "\","
        message_body += "\"hash\":" + "\"" + self.obj_hash + "\","
        message_body += "\"size\":" + "\"" + str(self.obj_size) + "\""
        message_body += "}]"
        message_body += "}"
        return message_body

    def generate_random_name(self, size):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    def generate_random_hash(self, size = 32):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))

    def get_ip_port_session(self):
        # src
        self.mac = random.choice(ReadFile.mac_ip_table.keys)
        self.src_ip = ReadFile.mac_ip_table.dict[self.mac]
        self.src_port = random.randint(1, 65535)
        # dst
        self.dst_ip = random.choice(ReadFile.file_ip_service_table.keys)
        self.service = ReadFile.file_ip_service_table.dict[self.dst_ip]
        self.dst_port = random.randint(1, 65535)
        self.session_id = random.randint(1, 999999)
        ip_seg = self.src_ip + ":" + str(self.src_port) + ":"
        ip_seg += self.dst_ip + ":" + str(self.dst_port) + ":" + str(self.session_id)
        return ip_seg

    def get_appname(self):
        return ReadFile.file_service_appname_table.dict[self.service]

    def get_sigid(self):
        return ReadFile.file_appname_sigid_table.dict[self.service]

    def get_host(self):
        return ReadFile.file_ip_host_table.dict[self.dst_ip]

    def get_url(self):
        return ReadFile.file_appname_url_table.dict[self.appname]

    def get_rspcode(self):
        return ReadFile.file_appname_rspcode_table.dict[self.appname]

    def push_log(self):
        log_output_name = "file_log.log"
        self.redis_connection.rpush(ReadConfiguration.aie_list_name, self.log)
        output(log_output_name, self.log)
