import random
from output import output
from read_configuration import ReadConfiguration
from table import Table

class AieVolumeLog:

    def __init__(self, aie_log):
        self.aie_log = aie_log

    def log_process(self):
        push_string = "{"
        #timestamp
        timestamp = self.aie_log.timestamp
        push_string += "\"timestamp\":" + "\"" + str(timestamp) + "\","
        #aie_id
        aie_id = ReadConfiguration.aie_id
        push_string += "\"aie_id\":" + "\"" + aie_id + "\","
        #request src_ip
        req_src = self.aie_log.src_ip
        push_string += "\"req_src\":" + "\"" + req_src + "\","
        #request port
        req_spt = self.aie_log.src_port
        push_string += "\"req_spt\":" + str(req_spt) + ","
        #response ip
        req_dst = self.aie_log.dst_ip
        push_string += "\"req_dst\":" + "\"" + req_dst + "\","
        #response port
        req_dpt = self.aie_log.dst_port
        push_string += "\"req_dpt\":" + str(req_dpt) + ","
        #request protocol
        req_proto = "tcp"
        push_string += "\"req_proto\":" + "\"" + req_proto + "\","
        #request volume
        #random bytes
        req_bytes = self.random_bytes()
        push_string += "\"req_bytes\":" + str(req_bytes) + ","
        #response volume
        #random bytes
        rsp_bytes = self.random_bytes()
        push_string += "\"rsp_bytes\":" + str(rsp_bytes) + ","
        #app layer protocol
        app_proto = "HTTP"
        push_string += "\"app_proto\":" + "\"" + app_proto + "\","
        #ssl
        ssl = "true"
        push_string += "\"ssl\":" + ssl + ","
        #duration
        duration = 1
        push_string += "\"duration\":" + str(duration) + ","
        #request hf latency
        req_hf_latency = random.randint(1, 100)
        push_string += "\"req_hf_latency\":" + str(req_hf_latency) + ","
        #response hf latency
        rsp_hf_latency = random.randint(1, 100)
        push_string += "\"rsp_hf_latency\":" + str(rsp_hf_latency) + ","
        #request ssl latency
        req_ssl_latency = random.randint(1, 100)
        push_string += "\"req_ssl_latency\":" + str(req_ssl_latency) + ","
        #request domain
        if hasattr(self.aie_log, 'host') :
            req_dn = self.aie_log.host
            push_string += "\"req_dn\":" + "\"" + req_dn + "\","
        else :
            req_dn = self.aie_log.table.get_item(self.aie_log.user.event, self.aie_log.user.appname, 'host')
            push_string += "\"req_dn\":" + "\"" + req_dn + "\","
        #domain acc
        dn_acc = "true"
        push_string += "\"dn_acc\":" + dn_acc + ","
        #appname
        appname = self.aie_log.user.appname
        push_string += "\"appname\":" + "\"" + appname + "\","
        #gw_id
        gw_id = ReadConfiguration.gw_id
        push_string += "\"gw_id\":" + "\"" + gw_id + "\""
        push_string += "}"
        #push string
        self.push_log(push_string)

    def push_log(self, push_string):
        self.aie_log.redis_connection.rpush(ReadConfiguration.aie_volume_list_name, push_string)
        output("aie_volume.log", push_string)
        return

    def random_bytes(self):
        ret_bytes = random.randint(100, 9999)
        return ret_bytes