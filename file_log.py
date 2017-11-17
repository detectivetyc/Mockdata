from aie_log import AieLog
from read_configuration import ReadConfiguration
from output import output
from read_sql import ReadSQL
from context_assemble import generate_body_part, generate_random_hash


class FileLog(AieLog):

    def get_sigid(self):
        return ReadSQL.get_event_sigid_from_sql(self.user.appname, self.table.activity_sql.list, self.user.event)
    def message_body_process(self, user):
        #use ReadSQL.get_element_by_sigid to get the context
        part_dict = generate_body_part(self.table.element_sql.list, self.sigid, user, self.table, self.session_id)
        message_body = "{"
        for key, value in part_dict.iteritems():
            if key == 'host' :
                self.host = value
                message_body += "\"host\":" + "\"" + self.host + "\","
            elif key == 'method' :
                self.method = value
                message_body += "\"method\":" + "\"" + self.method + "\","  # hard coded
            elif key == 'user_agent' :
                self.ua = value
                message_body += "\"user_agent\":" + "\"" + self.ua + "\","
            elif key == 'url' :
                self.url = value
                message_body += "\"url\":" + "\"" + self.url + "\","
            elif key == 'rsp_code' :
                self.rsp_code = value
                message_body += "\"rsp_code\":" + "\"" + self.rsp_code + "\","
            elif key == 'rsp_latency':
                self.rsp_latency = value
                message_body += "\"rsp_latency\":" + self.rsp_latency + ","
        # activity
        activity = ReadSQL.get_activity_name(self.sigid, self.table.activity_sql.list)
        message_body += "\"activity\":" + "\"" + activity[1 : len(activity) - 1] + "\","  # hard coded
        # objs
        # obj_type hard code?
        obj_type = "file"
        message_body += "\"objs\":[{" + "\"type\":" + "\"" + obj_type + "\","
        for key, value in part_dict.iteritems():
            if key == 'file_name' :
                self.file_name = value
                message_body += "\"name\":" + "\"" + self.file_name + "\","
            elif key == 'file_size' :
                self.file_size = value
                message_body += "\"size\":" + str(self.file_size) + ","
            elif key == 'file_hash' :
                self.file_hash = value
                message_body += "\"hash\":" + "\"" + self.file_hash + "\","
            elif key == 'session_id' :
                session_id = value
                message_body += "\"session_id\":" + "\"" + str(session_id) + "\","
        #special case for 0x4050000 and 0x4060000
        if self.sigid == "'0x4050000'" or self.sigid == "'0x4060000'":
            self.file_hash = generate_random_hash()
            message_body += "\"hash\":" + "\"" + self.file_hash + "\","
        message_body = message_body[0:len(message_body) - 1]
        message_body += "}]"
        message_body += "}"
        return message_body

    def push_log(self, log):
        log_output_name = "file_log.log"
        self.redis_connection.rpush(ReadConfiguration.aie_list_name, log)
        output(log_output_name, log)
