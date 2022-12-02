from AutoTh import AutoTh, Params, MachineInfo

autoth = AutoTh(username='ecnubc@163.com')

def open_machine(params):
    machine_info_list = autoth.submit(params=params)
    with open("name.txt", 'w', encoding="utf-8") as f:
        for machine_info in machine_info_list:
            f.write(machine_info.id + " " + machine_info.dir + " " + str(machine_info.url_id) +'\n')
        f.close()

# 这里写自己想要的机器名列表
# 示例：
# jobname = ["text-{}".format(i) for i in range(100)]
jobname = ["text-{}".format(i) for i in range(2)]
params = Params(jobname=jobname, cluster="k8s_venus", partition="venus-cpu", cpu=6, gpu=0, memory=30)

open_machine(params=params)