from aie_log import AieLog
from read_configuration import ReadConfiguration
from output import output
from read_sql import ReadSQL
from table import Table
from context_assemble import generate_body_part
import sys
class AppLog(AieLog):

    def message_body_process(self, user):
        part_dict = generate_body_part(self.table.element_sql.list, self.sigid, user, self.table, self.session_id)
        message_body = "{"
        for key, value in part_dict.iteritems():
            if key == 'host' :
                self.host = value
                message_body += "\"host\":" + "\"" + self.host.encode('utf8') + "\","
            elif key == 'url' :
                self.url = value
                message_body += "\"url\":" + "\"" + self.url.encode('utf8') + "\","
            elif key == 'method' :
                self.method = value
                message_body += "\"method\":" + "\"" + self.method + "\","
            elif key == 'user_agent' :
                self.ua = value
                message_body += "\"user_agent\":" + "\"" + self.ua.encode('utf8') + "\","
            elif key == 'rsp_code' :
                self.rsp_code = value
                message_body += "\"rsp_code\":" + "\"" + self.rsp_code.encode('utf8') + "\","
            elif key == 'rsp_latency' :
                self.rsp_latency = value
                message_body += "\"rsp_latency\":" + self.rsp_latency.encode('utf8') + ","
            else :
                sys.exit("No such context")
        message_body = message_body[0 : len(message_body) - 1]
        message_body += "}"
        return message_body

    def push_log(self, log):
        log_output_name = "app_log.log"
        self.redis_connection.rpush(ReadConfiguration.aie_list_name, log)
        output(log_output_name, log)

