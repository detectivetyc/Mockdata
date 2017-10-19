from aie_log import AieLog
from read_configuration import ReadConfiguration
from output import output

class AppLog(AieLog):

    def message_body_process(self):
        #rsp_latency
        self.rsp_latency = '1' #hard coded
        #rsp_code
        self.rsp_code = self.get_rspcode()
        #host got from AieLog::log_process
        #method
        self.method = "POST"
        #url got from AieLog::log_process
        message_body = "{"
        message_body += "\"host\":" + "\"" + self.host + "\","
        message_body += "\"method\":" + "\"" + self.method + "\","
        message_body += "\"url\":" + "\"" + self.url + "\","
        message_body += "\"user_agent\":" + "\"" + self.ua + "\","
        message_body += "\"rsp_code\":" + "\"" + self.rsp_code + "\","
        message_body += "\"rsp_latency\":" + "\"" + self.rsp_latency +"\","
        message_body += "}"
        return message_body

    def push_log(self):
        log_output_name = "app_log.log"
        self.redis_connection.rpush(ReadConfiguration.aie_list_name, self.log)
        output(log_output_name, self.log)

