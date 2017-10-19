from aie_log import AieLog
from read_configuration import ReadConfiguration
from output import output

class LoginLog(AieLog):

    def message_body_process(self):
        # host got from AieLog::log_process
        # method
        self.method = "GET"
        # url got from AieLog::log_process
        # ua got from AieLog::log_process
        # rsp_code got from AieLog::log_process
        # login_name
        self.login_name = "tony@holonetsecurity.com"

        message_body = "{"
        message_body += "\"host\":" + "\"" + self.host + "\","
        message_body += "\"method\":" + "\"" + self.method + "\","
        message_body += "\"url\":" + "\"" + self.url + "\","
        message_body += "\"login_name\":" + "\"" + self.login_name + "\","
        message_body += "\"user_agent\":" + "\"" + self.ua + "\","
        message_body += "\"rsp_code\":" + "\"" + self.rsp_code + "\","
        message_body += "\"success\":" + "true"
        message_body += "}"

        return message_body
    def push_log(self):
        log_output_name = "login_log.log"
        self.redis_connection.rpush(ReadConfiguration.aie_list_name, self.log)
        output(log_output_name, self.log)