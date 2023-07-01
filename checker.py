import requests
import config
import os
import yaml
import json

defalut_config = \
f"""allow-lan: true
external-controller: :{config.clash_controller_port}
log-level: info
mode: Global
port: {config.clash_http_port}"""


def switchProxy(name):
    switch = requests.put(f"http://127.0.0.1:{config.clash_controller_port}/proxies/GLOBAL",data = json.dumps({"name":name}))
    if switch.status_code == 204:
        return True
    else:
        return False
    

def check_clash():
    try:
        a = requests.get(f"http://{config.remote_host}:{config.clash_controller_port}/")
        print("clash 服务已启动")
        return True
    except:
        print("clash 服务未启动")
        return False

def ping():
    proxy = {
        "http":f"http://127.0.0.1:{config.clash_http_port}",
        "https":f"http://127.0.0.1:{config.clash_http_port}"
    }
    try:
        headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
        r = requests.get("https://www.google.com/",timeout = 5,proxies=proxy,headers=headers)
        if r.status_code == 200:
            print("代理正常")
            return True
        else:
            print("代理异常")
            return False
    except:
        print("代理异常 - 无法连接")
        return False

def check(clash_config):
    if check_clash():
        default = yaml.safe_load(defalut_config)
        default['proxies'] = [clash_config]
        with open("./temp.yaml","w",encoding="utf-8") as f:
            yaml.dump(default,f)
        print("开始刷新配置")
        current_path = os.path.abspath(__file__)
        config_file_path=os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + 'temp.yaml'))
        r = requests.put(f"http://127.0.0.1:{config.clash_controller_port}/configs",data = json.dumps({"path":config_file_path}))
        print(f"配置刷新完成 - {r.status_code}")
        if r.status_code == 204:
            switchProxy(default['proxies'][0]['name'])
            if ping():
                return True
            else:
                return False
        else:
            return False
    else:
        raise Exception("clash 服务未启动")

def get_remote_country():
    proxy = {
        "http":"http://127.0.0.1:7890",
        "https":"http://127.0.0.1:7890"
    }
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    try:
        a = requests.get(f"https://api.ip.sb/geoip/",headers = headers,proxies=proxy).json()
        a = a['country_code']
        return a
    except:
        return "Unknown"