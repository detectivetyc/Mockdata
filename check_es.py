import elasticsearch

class CheckES():

    def __init__(self, host, target_log):
        try:
            self.es = elasticsearch.Elasticsearch(host)
        except (elasticsearch.ConnectionError, elasticsearch.ConnectionTimeout):
            print "ElasticSearch Instance establish failed."
        self.log = target_log
        self.index = self.get_index(self.log.timestamp)


    def get_index(self, timestamp):
        return '107-aie-' + timestamp.split('-')[0] + '.' + timestamp.split('-')[1]

    def check_log_exist(self):
        try:
            total = self.es.search(index=self.index,
                                   body={"query":
                                             {"bool":
                                                  {"must":
                                                       [{"match":{"sess_id":self.log.session_id}},
                                                        {"match":{"src_port":self.log.src_port}},
                                                        {"match":{"dst_port":self.log.dst_port}}]}}})['hits']['total']
        except elasticsearch.RequestError:
            print "Request Error!"
        else:
            print "search success."
            return total
