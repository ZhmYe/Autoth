import requests
import json
from tqdm import tqdm
from submit import submit_request
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
        self.submit_requst = submit_request(self.token)
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
            submit_payload = self.submit_requst.get_payload(jobname=jobname,  cluster=params.cluster, partition=params.partition, cpu=params.cpu, gpu=params.gpu, memory=params.memory)
            response = requests.post('https://starlight.nscc-gz.cn/api/job/submit', headers=self.submit_requst.get_post_headers(),data=submit_payload)
            txt = json.loads(response.text)['spec']
            # print(txt)
            # requests.get('https://starlight.nscc-gz.cn/api/job/running/k8s_venus/{}'.format(machine_info.id), headers=self.submit_requst.get_get_headers())
            # print(spec)
            spec= json.loads(requests.get('https://starlight.nscc-gz.cn/api/job/running/k8s_venus/{}'.format(txt["cluster_job_id"]), headers=self.submit_requst.get_get_headers()).text)['spec']
            final_response = requests.post('https://starlight.nscc-gz.cn/api/label/proxy/available', headers=self.submit_requst.get_post_headers(), data=json.dumps(spec['proxies']))
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