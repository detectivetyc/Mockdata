from read_configuration import ReadConfiguration
from context_assemble import generate_random_hash, generate_random_name
from output import output
import random
class ContentScanLog():
    def __init__(self, table, file_log, risk=None):
        self.table = table
        self.file_log = file_log
        if risk is not None:
            self.risk = risk

    def log_process(self):
        push_string = "{\"objs\":[{"
        # id
        id = 0
        push_string += "\"id\":" + str(id) + ","
        #hash
        if hasattr(self.file_log, 'file_hash'):
            file_hash = self.file_log.file_hash
        else:
            file_hash = generate_random_hash()
        push_string += "\"hash\":\"" + file_hash + "\","
        #obj_type (?)
        self.obj_type = 'text/xml'
        push_string += "\"obj_type\":\"" + self.obj_type + "\","
        # file name
        if hasattr(self.file_log, 'file_name'):
            file_name = self.file_log.file_name
        else:
            file_name = generate_random_name()
        push_string += "\"name\":\"" + file_name + "\","
        #subfile
        if self.file_log.user.subfile is not None:
            push_string += "\"subfile\":\"" + self.file_log.user.subfile + "\","
        #type
        type = 'file'
        push_string += "\"type\":\"" + type + "\","
        #size
        if hasattr(self.file_log, 'file_size'):
            file_size = self.file_log.file_size
        else:
            file_size = random.randint(1000, 99999)
        push_string += "\"size\":" + str(file_size) + ","
        #risk_groups
        group_name = self.table.name_group_dict[self.file_log.user.pattern_name]
        push_string += "\"risk_groups\":" + "[\"" + group_name + "\"],"
        #match_groups
        push_string += "\"match_groups\":" + "[{\"group\":\"" + group_name + "\",\"name\":\"" +  self.file_log.user.pattern_name + "\"}]"
        push_string += "}],"
        #gw_id
        gw_id = ReadConfiguration.gw_id
        push_string += "\"gw_id\":\"" + gw_id + "\","
        #aie_id
        aie_id = ReadConfiguration.aie_id
        push_string += "\"aie_id\":\"" + aie_id + "\","
        #session_id
        session_id = self.file_log.session_id
        push_string += "\"sess_id\":" + str(session_id)
        push_string += "}"

        self.push_log(push_string)

    def push_log(self, log):
        log_output_name = "content_scan.log"
        self.file_log.redis_connection.rpush(ReadConfiguration.content_scan_list_name, log)
        output(log_output_name, log)
