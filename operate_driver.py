from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import argparse
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")
# 批量打开机器open_machine,params: [number:打开机器的数量, save_name: 是否保存当前开启的机器名, save_path: 机器名文件保存路径]
# 关于保存机器名的原因见close_machine函数
def open_machine(number=3, save_name=False, save_path='name.txt', gpu=False, config=6):
    name_list = []
    for i in tqdm(range(number)):
        driver.get(r'https://starlight.nscc-gz.cn/#/app/spec/ubuntu1804?type=2&id=605') # 进入Ubuntu机器创建界面
        while (True):
            try:
                # 选择分区venus-cpu,如果是venus-gpu将最后的label[2]改为label[1]
                driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/section/div/div[2]/div/div[1]/div/div[1]/div/div/div[2]/div[2]/div/form/div[4]/div/div/form/div/div/div/div/div/label[{}]'.format(1 if gpu else 2)).click()
                time.sleep(1) # 考虑到下面的配置元素是根据上面的分区选择改变通过脚本重新加载得到的，为避免加载延迟
                # 选择作业配置6核30GB，其它配置根据顺序修改最后的label[x]
                driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/section/div/div[2]/div/div[1]/div/div[1]/div/div/div[2]/div[2]/div/form/div[5]/div/div/form/div/div/div/div/div/label[{}]'.format(config_dic[gpu][config])).click()
                break
            except:
                pass
        time.sleep(1) # 确保选择完上面的配置后，前端js脚本已经获取到对应的参数
        while (True):
            try:
                # 点击提交作业按钮
                driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/section/div/div[2]/div/div[1]/div/div[2]/div/div/button').click()
                break
            except:
                pass
        time.sleep(1) # 确保任务流程执行完毕
        if save_name:
            while (True):
                try:
                    # 爬取机器名
                    name = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/section/div/div[2]/div[1]/div[1]/div/span').text #获取机器名
                    # print(name)
                    name_list.append(name)
                    time.sleep(1)
                    break
                except:
                    pass
    if save_name:
        # 将所有机器名保存到文件中
        with open(save_path, 'w', encoding='utf-8') as f:
            for name in name_list:
                f.write(name + '\n')
            f.close()

# 批量关闭机器close_machine,params: [file_path: 机器名文件路径]
def close_machine(file_path='name.txt'):
    # 考虑到如果直接使用xpath来关闭机器，可能会关闭其他人开启的机器(无法在前端区分)，所以最好是给出一个"我"开启的机器名，然后一一关闭
    # 机器名文件可以通过open_machine中的save_path来更改，默认为'name.txt'
    with open(file_path, encoding='utf-8') as f:
        name_list = f.read().split("\n")[:-1] # 获取所有机器名
    for name in tqdm(name_list):
        # 进入对应的作业管理网页
        driver.get('https://starlight.nscc-gz.cn/#/job/info/k8s_venus/{}'.format(name))
        while (True):
            try:
                # 点击关闭作业
                driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/section/div/div[2]/div[4]/div[2]/button[1]').click()
                time.sleep(1)
                break
            except:
                pass
        while (True):
            try:
                # 点击确定
                driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/button[2]').click()
                time.sleep(1)
                break
            except:
                pass

# 删除存储delete_memory,params: [file_path: 机器名文件路径, delete_dir_name: 删除的文件夹名]
# 该函数只适用于/GPUFS/app/bihu/spooler/机器名/只有一个文件夹
def delete_memory(file_path='name.txt', delete_dir_name='fisco'):
    with open(file_path, encoding='utf-8') as f:
        name_list = f.read().split("\n")[:-1] # 获取所有机器名
    for name in tqdm(name_list):
        driver.get('https://starlight.nscc-gz.cn/#/job/info/k8s_venus/{}?history=true'.format(name))
        # driver.get('https://starlight.nscc-gz.cn/#/job/info/k8s_venus/ubuntu1804-31141857?history=true')
        time.sleep(2) # 确保加载完成
        element = None
        try:
            # 只要能保证/GPUFS/app/bihu/spooler/机器名/下面只有一个文件夹
            # 那么要删除的文件夹的名字就是当前要点击的element的id且下面的各元素的xpath是确定正确的
            element = driver.find_element_by_id(delete_dir_name) 
        except:
            pass
        if element is not None:
            while (True):
                try:
                    # 右击要删除的文件夹所对应的element
                    ActionChains(driver=driver).context_click(element).perform()
                    # 点击弹出的下拉菜单中的删除
                    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[6]/div/div[2]/div[2]/div/body/div/div/span[3]').click()
                    break
                except:
                    pass
            time.sleep(2) # 等待确认弹窗
            # 点击确认
            driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/section/div/div[4]/div/div[3]/div/div[3]/span/button[2]').click()
            time.sleep(1)

# 批量打开浏览器上的shell并统一输入命令key_bash, params: [file_path: 机器名文件, bash_content: 输入的命令]
# 这里可以在机器根目录(所有机器共用)下先写一个.sh文件，将要执行的命令写在里面,然后统一输入'bash .sh'来达到类似统一启动的效果
def key_bash(file_path='name.txt', bash_content=''):
    with open(file_path, encoding='utf-8') as f:
        name_list = f.read().split("\n")[:-1] # 获取所有机器名
    for name in tqdm(name_list):
        # 进入机器对应的作业管理界面
        driver.get('https://starlight.nscc-gz.cn/#/job/info/k8s_venus/{}'.format(name))
        while(True):
            try:
                # 获取下面的shell url
                url = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/section/div/div[6]/div/ul/li[2]/div/div[1]/a/span').text
                # 进入shell界面
                driver.get(url)
                time.sleep(10) #有zsh的安装？
                break
            except:
                pass  
        while(True):
            try:
                # 输入命令
                driver.find_element_by_xpath('//*[@id="terminal-container"]/div').send_keys(bash_content + Keys.ENTER)
                time.sleep(2)
                break
            except:
                pass  
# open_machine(number=1, save_name=True)
# close_machine()
if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-r', type=str, default="open", help='open, close, delelte, key')
    parse.add_argument('-n', type=int, default=1, help='machine number')
    parse.add_argument('-p', type=str, default='name.txt', help='file path to save names')
    parse.add_argument('-s', action='store_true', default=False, help='save names or not')
    parse.add_argument('-b', type=str, default='', help='bash content to key')
    parse.add_argument('-d', type=str, default='', help='dir name to delete')
    parse.add_argument('-c', type=int, default=6, help='cpu number')
    parse.add_argument('-g', action='store_true', default=False, help='use gpu or not')
    opt = parse.parse_args()
    assert (opt.r in ['open', 'close', 'delete', 'key']), 'only support run type in [open, close, delete, key]'
    option = webdriver.ChromeOptions() 
    # option.add_argument('headless') # 隐藏窗口，因为有时候会出现加载问题导致脚本卡住还是人为看着比较合适，建议注释（尤其是开启机器数量较多时）
    config_dic = {
        True: {6: 1, 12: 2},
        False: {1: 1, 6: 2, 12: 3, 36: 4}
    }
    assert (config_dic[opt.g][opt.c]), 'no such config'
    # todo 修改这里的ChromeDriver路径
    driver = webdriver.Chrome(executable_path=r'D:/document/codeapi/chromedriver_win32/chromedriver.exe',chrome_options=option)
    driver.implicitly_wait(10) # 隐式等待，等待网页加载完成，最大等待时间为10s

    driver.get(r'https://starlight.nscc-gz.cn/#/login') #打开天河平台登录界面
    while (True): #这里的循环是为了防止网络加载导致加载不下面xpath的element
        try:
            driver.find_element_by_xpath("/html/body/div/div/form/div[3]/div/div/input").send_keys("你的账号") # 输入账号
            driver.find_element_by_xpath("/html/body/div/div/form/div[5]/div/div/input").send_keys("你的密码") # 输入密码
            driver.find_element_by_xpath("/html/body/div/div/form/button").click() #点击登录按钮
            break
        except:
            pass
    # 登录天河平台后会出现一个遮罩层(引导步骤),需要关闭
    while (True):
        try:
            driver.find_element_by_xpath('//*[@id="driver-popover-item"]/div[4]/button').click()
            break
        except:
            pass
    if opt.r == 'open':
        open_machine(number=opt.n, save_name=opt.s, save_path=opt.p, gpu=opt.g, config=opt.c)
    elif opt.r == 'close':
        close_machine(file_path=opt.p)
    elif opt.r == 'delete':
        delete_memory(file_path=opt.p, delete_dir_name=opt.d)
    else:
        key_bash(file_path=opt.p, bash_content=opt.b)
    driver.quit()
