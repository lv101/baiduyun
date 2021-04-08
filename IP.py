import requests


def get_ip(ip):
    url = "https://www.ip.cn/api/index"
    params = {
        "ip": ip,
        "type": 1
    }
    try:
        r = requests.get(url=url, params=params, timeout=10)
        ip = r.json()['ip']
        address = r.json()['address'].split()
        # print(f'IP：{ip}\nINFO：{address}')
        return address
    except:
        return
        # print("查询失败")