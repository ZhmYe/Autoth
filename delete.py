import json
class delete_request:
    def __init__(self, token):
        self.token = token
    def get_headers(self):
        self.headers = {
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
        return self.headers