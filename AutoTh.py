import requests
import json
from tqdm import tqdm
from submit import submit_request
from delete import delete_request
from storage import storage_request
# from shell import shell_request
from MyWebSocket import websocketInstance 
class Params:
    def __init__(self, jobname, cluster, partition, cpu, gpu, memory):
        self.jobname = jobname
        self.cluster = cluster
        self.partition = partition
        self.cpu = cpu
        self.gpu = gpu
        self.memory = memory
        self.number = len(self.jobname)
class MachineInfo:
    def __init__(self, id, dir, url_id):
        self.id = id
        self.dir = dir
        self.url_id = url_id

class AutoTh:
    def __init__(self, username):
        self.username = username
        self.get_token()
        self.submit_request = submit_request(self.token)
        self.delete_request = delete_request(self.token)
        self.storage_request = storage_request(self.token)
        # self.shell_requset = shell_request(self.token)
        # self.url = url
    def get_token(self):
        name_payload = {"username":self.username,"password":"RWNudWJsb2NrY2hhaW4=","token_type":'null',"cookie_exp":'null',"redirect_url":'null'}
        # print(str(name_payload))
        response = requests.post("https://starlight.nscc-gz.cn/api/keystone/short_term_token/name", data=json.dumps(name_payload))
        # print(response.text)
        self.token = json.loads(response.text)['spec']
        return self.token
    def submit(self, params):
        print("-------------------Submit-------------------")
        print("Params: ")
        print("     number: ", params.number)
        # print("     jobname: ", params.jobname)
        print("     cluster: ",  params.cluster)
        print("     partition: ", params.partition)
        print("     cpu: ", params.cpu)
        print("     gpu: ", params.gpu)
        print("     memory: ", params.memory)
        status_code = {}
        machine_info_list = []
        for jobname in  tqdm(params.jobname):
            submit_payload = self.submit_request.get_payload(jobname=jobname,  cluster=params.cluster, partition=params.partition, cpu=params.cpu, gpu=params.gpu, memory=params.memory)
            response = requests.post('https://starlight.nscc-gz.cn/api/job/submit', headers=self.submit_request.get_post_headers(),data=submit_payload)
            txt = json.loads(response.text)['spec']
            # print(txt)
            # requests.get('https://starlight.nscc-gz.cn/api/job/running/k8s_venus/{}'.format(machine_info.id), headers=self.submit_request.get_get_headers())
            # print(spec)
            spec= json.loads(requests.get('https://starlight.nscc-gz.cn/api/job/running/k8s_venus/{}'.format(txt["cluster_job_id"]), headers=self.submit_request.get_get_headers()).text)['spec']
            final_response = requests.post('https://starlight.nscc-gz.cn/api/label/proxy/available', headers=self.submit_request.get_post_headers(), data=json.dumps(spec['proxies']))
            if final_response.status_code == 200:
                machine_info_list.append(MachineInfo(txt["cluster_job_id"], txt["work_dir"], spec['proxies'][1]["id"]))
            if final_response.status_code in status_code:
                status_code[final_response.status_code] += 1
            else:
                status_code[final_response.status_code] = 1
        print("\nResult: ")
        print("     response Status Code: ")
        for code in status_code:
            print("         {}: {} / {}".format(code, status_code[code], len(params.jobname)))
        print("-------------------Submit END-------------------")
        return machine_info_list
    def delete(self, params):
        print("-------------------Delete-------------------")
        print("Params: ")
        print("     number: ", params.number)
        # print("     jobname: ", params.jobname)
        print("     cluster: ",  params.cluster)
        print("     partition: ", params.partition)
        status_code = {}
        headers = self.delete_request.get_headers()
        for jobname in tqdm(params.jobname):
            response = requests.delete('https://starlight.nscc-gz.cn/api/job/running/k8s_venus/{}'.format(jobname), headers=headers)
            if response.status_code in status_code:
                status_code[response.status_code] += 1
            else:
                status_code[response.status_code] = 1
        print("\nResult: ")
        print("     response Status Code: ")
        for code in status_code:
            print("         {}: {} / {}".format(code, status_code[code], len(params.jobname)))
        print("-------------------Delete END-------------------")
    def delete_storage(self, params, dir):
        print("-------------------Delete Storage-------------------")
        print("Params: ")
        print("     number: ", params.number)
        # print("     jobname: ", params.jobname)
        print("     cluster: ",  params.cluster)
        print("     partition: ", params.partition)
        status_code = {}
        for jobname in tqdm(params.jobname):
            payload = self.storage_request.get_payload(jobname=jobname, dir=dir)
            response = requests.post('https://starlight.nscc-gz.cn/api/storage/opt', headers=self.storage_request.get_headers(),data=payload)
            if response.status_code in status_code:
                status_code[response.status_code] += 1
            else:
                status_code[response.status_code] = 1
        print("\nResult: ")
        print("     response Status Code: ")
        for code in status_code:
            print("         {}: {} / {}".format(code, status_code[code], len(params.jobname)))  
        print("-------------------Delete Storage END-------------------")
    def get_shell(self, url):
        print("-------------------Start Shell-------------------")
        t = tqdm(url)
        for prefix in t:
            # print("get shell in url: http://{}.proxy.nscc-gz.cn:8888...".format(prefix))
            t.set_description("http://{}.proxy.nscc-gz.cn:8888".format(prefix))
            self.wsi = websocketInstance(prefix)
            self.wsi.run()
        print("-------------------Start Shell END-------------------")
        # ws.keep_running=False
        # ws.run_forever()
    def get_ip(self, url):
        response = requests.get(url, headers=self.submit_request.get_get_headers())
        # print(json.loads(response.text)['spec'][0])
        try:
            ip = json.loads(response.text)['spec'][0]['name']
            return ip
        except:
            raise AssertionError("dir info error")