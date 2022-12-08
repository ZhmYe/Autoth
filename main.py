from AutoTh import AutoTh, Params, MachineInfo
import argparse
from config import Config
from userFunction import get_open_job_name, get_close_job_name, get_dir_name, get_url
autoth = AutoTh(username='ecnubc@163.com')

def open_machine(params):
    machine_info_list = autoth.submit(params=params)
    with open("name.txt", 'w', encoding="utf-8") as f:
        for machine_info in machine_info_list:
            f.write(machine_info.id + " " + machine_info.dir + " " + str(machine_info.url_id) +'\n')
        f.close()
def delete_machine(params):
    autoth.delete(params=params)


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-r', type=str, default="open", help='open, close')
    opt = parse.parse_args()
    assert (opt.r in ['open', 'close', 'storage', 'shell']), 'only support run type in [open, close, storage, shell]'
    CONFIG = Config()
    if opt.r == "open":    
        CONFIG.print()
        config = CONFIG.choose(index=int(input("key the index of the config you choose:")))
        jobname = get_open_job_name()
        params = Params(jobname=jobname, cluster="k8s_venus", partition="venus-cpu", cpu=config["cpu"], gpu=config["gpu"], memory=config["memory"])
        open_machine(params=params)
    if opt.r == "close":
        machine_data = get_close_job_name()
        params = Params(jobname=machine_data, cluster="k8s_venus", partition="venus-cpu", cpu=None, gpu=None, memory=None)
        autoth.delete(params=params)
    if opt.r == "storage":
        machine_data = get_close_job_name()
        params = Params(jobname=machine_data, cluster="k8s_venus", partition="venus-cpu", cpu=None, gpu=None, memory=None)
        dir_list = get_dir_name()
        for dir in dir_list:
            print("delete dir [{}]...".format(dir))
            autoth.delete_storage(params=params, dir=dir)
    if opt.r == "shell":
        url_list = get_url()
        autoth.get_shell(url_list)
        