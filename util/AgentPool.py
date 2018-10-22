import requests
import json
import time

class AgentPool:
    def __init__(self):
        self.daxiang_agent_source = "http://tpv.daxiangdaili.com/ip/?tid=555073632194763&num=1&&filter=on&protocol=https&delay=5&sortby=speed&format=json"
        self.data5u_agent_source = "http://api.ip.data5u.com/dynamic/get.html?order=b2dbc800b7111a3c842407f9165dfa14&sep=3"

    def get_daxiang_agent(self):
        res = requests.get(self.daxiang_agent_source)
        res_json = json.loads(res.text)
        ip = res_json[0].get("host")
        port = res_json[0].get("port")
        return "%s:%s" % (ip, port)

    def get_data5u_agent(self):
        time.sleep(1)
        res = requests.get(self.data5u_agent_source)
        return res.text

