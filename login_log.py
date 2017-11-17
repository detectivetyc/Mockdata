from aie_log import AieLog
from read_configuration import ReadConfiguration
from output import output
import sys
from read_sql import ReadSQL
from context_assemble import generate_body_part

class LoginLog(AieLog):

    def get_sigid(self):
        return ReadSQL.get_event_sigid_from_sql(self.user.appname, self.table.activity_sql.list, 'login')
    def message_body_process(self, user):
        #use ReadSQL.get_element_by_sigid make sure which part is required
        part_dict = generate_body_part(self.table.element_sql.list, self.sigid, user, self.table, self.session_id)
        message_body = "{"
        for key, value in part_dict.iteritems() :
            if key == 'host' :
                self.host = value
                message_body += "\"host\":" + "\"" + self.host.encode('utf8') + "\","
            elif key == 'url' :
                self.url = value
                message_body += "\"url\":" + "\"" + self.url.encode('utf8') + "\","
            elif key == 'method' :
                self.method = value
                message_body += "\"method\":" + "\"" + self.method.encode('utf8') + "\","
            elif key == 'user_agent' :
                self.ua = value
                message_body += "\"user_agent\":" + "\"" + self.ua.encode('utf8') + "\","
            elif key == 'rsp_code' :
                self.rsp_code = value
                message_body += "\"rsp_code\":" + "\"" + self.rsp_code.encode('utf8') + "\","
            elif key == 'login_name':
                self.login_name = value
                message_body += "\"login_name\":" + "\"" + self.login_name.encode('utf8') + "\","
            elif key == 'user_name@b64':
                self.login_name = value
                message_body += "\"login_name\":" + "\"" + self.login_name.encode('utf8') + "\","
            elif key == 'rsp_latency':
                self.rsp_latency = value
                message_body += "\"rsp_latency\":" + self.rsp_latency.encode('utf8') + ","
            elif key == 'session_id':
                message_body += "\"session_id\":" + "\"" + str(self.session_id) + "\","
            elif key == 'status_code':
                self.rsp_code = value
                message_body += "\"status_code\":" + "\"" + self.rsp_code.encode('utf8') + "\","
            elif key == 'user_id':
                userid = value
                message_body += "\"user_id\":" + "\"" + str(userid) + "\","
            elif key == 'user_token':
                user_token = value
                message_body += "\"user_token\":" + "\"" + user_token + "\","
            else :
                sys.exit("No such context")
        message_body += "\"success\":" + "true"
        message_body += "}"

        return message_body

    def push_log(self, log):
        log_output_name = "login_log.log"
        self.redis_connection.rpush(ReadConfiguration.aie_list_name, log)
        output(log_output_name, log)