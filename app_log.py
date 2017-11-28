from aie_log import AieLog
from read_configuration import ReadConfiguration
from output import output
from read_sql import ReadSQL
from table import Table
from context_assemble import generate_body_part
import sys
class AppLog(AieLog):

    def message_body_process(self, buffer):
        self.generate_body_part(buffer)

    def push_log(self, log):
        log_output_name = "app_log.log"
        self.redis_connection.rpush(ReadConfiguration.aie_list_name, log)
        output(log_output_name, log)

