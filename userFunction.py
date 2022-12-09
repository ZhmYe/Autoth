def get_open_job_name():
    # 这里写自己想要的机器名列表
    # 示例：
    # jobname = ["text-{}".format(i) for i in range(100)]
    jobname = ["text-{}".format(i) for i in range(1)]
    return jobname
def get_close_job_name():
    # 这里写自己想要删除的机器名列表
    # 示例： 从保存的name.txt中读取所有机器名
    with open("name.txt", 'r', encoding='utf-8') as f:
        machine_data = f.read().split("\n")
        f.close()
    while (True):
        try:
            machine_data.remove('')
        except:
            break
    machine_data = [data.split(" ")[0] for data in machine_data]
    return machine_data
def get_dir_name():
    # 这里写自己想要删除的文件夹名列表
    return ["ip"]
def get_url():
    # 这里得到shell的url前面的前缀数字列表
    # 如http://260547.proxy.nscc-gz.cn:8888/ 前面的260547
    with open("name.txt", "r", encoding="utf-8") as f:
        machine_data = f.read().split("\n")
        f.close()
    while (True):
        try:
            machine_data.remove('')
        except:
            break
    url = [data.split(" ")[2] for data in machine_data]
    return url
def operate_process(autoth):
    # 自定义在连接shell后，机器运行shell启动脚本后后续要做的操作
    machine_name = get_close_job_name()
    url_dic = {name: 'https://starlight.nscc-gz.cn/api/storage/dir_info?dir=/GPUFS/app/bihu/spooler/{}/ip&sort_key=time&order_by=desc'.format(name) for name in machine_name}
    ip_dic = {}
    for name in url_dic:
        url = url_dic[name]
        ip = autoth.get_ip(url)
        ip_dic[name] = ip
    with open("ip.txt", 'w', encoding="utf-8") as f:
        for name in ip_dic:
            f.write("{} {}\n".format(name, ip_dic[name]))
