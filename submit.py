# import requests
import json
class submit_request:
    def __init__(self, token) -> None:
        self.token = token
    def get_payload(self, jobname, cluster="k8s_venus", partition="venus-cpu", cpu=6, gpu=0, memory=30):
        submit_payload =  {
                                "app":"ubuntu1804",
                                "params":{},
                                "runtime_params":{"0":"{","1":'"',"2":"u","3":"s","4":"e","5":"r","6":"M","7":"o","8":"d","9":"e","10":'"',"11":":","12":'"',"13":'"',"14":",","15":'"',"16":"e","17":"n","18":"d","19":"p","20":"o","21":"i","22":"n","23":"t","24":"s","25":'"',"26":":","27":"[","28":"]","29":",","30":'"',"31":"e","32":"n","33":"v","34":'"',"35":":","36":"{","37":"}","38":"}",
                                                "endpoints":[{"control":3,"domain":'null',"name":"ssh-default","protocol":3,"target_port":22,"type":1},
                                                            {"control":3,"domain":'null',"name":"ttyd-user","protocol":1,"target_port":7681,"type":1}],
                                                            "env":{"LDAP_SERVER":"ldap://89.72.30.1/"},
                                                            "jobname": jobname,
                                                            "image":"hub.starlight.nscc-gz.cn/nsccgz_duliang_1_public/ubuntu-1606286629:18.04",
                                                            "cluster": cluster,
                                                            "partition": partition,
                                                            "_resources": json.dumps({"cpu":cpu,"gpu":gpu,"memory":memory}),
                                                            "cpu": cpu,
                                                            "gpu": gpu,
                                                            "memory": memory}}

        self.payload = json.dumps(submit_payload)
        return self.payload
    def get_post_headers(self):
        self.post_headers = {
            'Accept': "application/json",
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Bihu-Token': self.token,
            'Connection': 'keep-alive',
            'Content-Length': str(len(json.dumps(self.payload))),
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'Bihu-Token={}; sidebarStatus=0'.format(self.token),
            'Host': 'starlight.nscc-gz.cn',
            'Origin': 'https://starlight.nscc-gz.cn',
            'Referer': 'https://starlight.nscc-gz.cn/',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TIMEOUT': '100',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return self.post_headers
    def get_get_headers(self):
        self.get_headers = {
            'Accept': "application/json",
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Bihu-Token': self.token,
            'Connection': 'keep-alive',
            'Cookie': 'Bihu-Token={}; sidebarStatus=0'.format(self.token),
            'Host': 'starlight.nscc-gz.cn',
            'Origin': 'https://starlight.nscc-gz.cn',
            'Referer': 'https://starlight.nscc-gz.cn/',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TIMEOUT': '100',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        return self.get_headers
# response = requests.post('https://starlight.nscc-gz.cn/api/job/submit', headers=headers,data=submit_payload)