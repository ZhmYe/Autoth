# import requests
import json
class storage_request:
    def __init__(self, token) -> None:
        self.token = token
    def get_payload(self, jobname, dir):
        payload = {
                    "type": 1,
                    "target": [ {"path":"/GPUFS/app/bihu/spooler/{}/{}".format(jobname, dir)} ]
                  }
        self.payload = json.dumps(payload)
        return self.payload
    def get_headers(self):
        assert (self.payload is not None), 'Please get payload first...'
        self.headers = {
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
        return self.headers