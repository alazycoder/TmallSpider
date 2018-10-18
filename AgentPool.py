import requests
import json


class AgentPool:
    def __init__(self):
        self.agent_source = "http://tpv.daxiangdaili.com/ip/?tid=555073632194763&num=1&&filter=on&protocol=https&delay=5&sortby=speed&format=json"

    def get_agent(self):
        res = requests.get(self.agent_source)
        res_json = json.loads(res.text)
        ip = res_json[0].get("host")
        port = res_json[0].get("port")
        return "%s:%s" % (ip, port)
