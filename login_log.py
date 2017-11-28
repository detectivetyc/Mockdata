from aie_log import AieLog
from read_configuration import ReadConfiguration
from output import output
import sys
from read_sql import ReadSQL
from context_assemble import generate_body_part

class LoginLog(AieLog):

    def get_sigid(self):
        return ReadSQL.get_event_sigid_from_sql(self.user.appname, self.table.activity_sql.list, 'login')

    def message_body_process(self, buffer):
        #use ReadSQL.get_element_by_sigid make sure which part is required
        self.generate_body_part(buffer)


    def push_log(self, log):
        log_output_name = "login_log.log"
        self.redis_connection.rpush(ReadConfiguration.aie_list_name, log)
        output(log_output_name, log)