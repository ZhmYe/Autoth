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
