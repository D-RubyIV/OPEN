
from time import sleep
import requests, random


class ProxyWheel():
    def __init__(self) -> None:
        pass
    def getNewIp(self, api_key):
        headers = {
        "Accept":"application/json",
        "Content-Type":"application/json",
        }
        ip_me = requests.get('https://api.ipify.org/?format=json', headers=headers).json()["ip"]
        if '|' in api_key:
            ipp, port, user, pas_ = api_key.split(":",3)
            pas_, linkchange = pas_.split('|')
            while True:
                change_ip = requests.get(linkchange, headers=headers).json()
                sleep(5)
                if change_ip['status'] == True:
                    ip = f"http://{user}:{pas_}@{ipp}:{port}"
                    proxies = {"http": ip , "https": ip}
                    return ip, proxies
                else:
                    sleep(5)
        elif str(api_key).count("-") == 5:
            print('WWWW')
            while True:
                listProvine = [i["id"] for i in requests.get("https://wwproxy.com/api/client/province?search_text=").json()["data"]]
                ip = requests.get(f"https://wwproxy.com/api/client/proxy/available?key={api_key}&provinceId={random.choice(listProvine)}").json()
                print(ip)
                if ip["errorCode"] == 0:
                    ipcc = ip['data']['proxy']
                    proxies = {"http": ipcc , "https": ipcc}
                    return ipcc, proxies
                elif ip["errorCode"] == 1:
                    for ll in range(20, -1, -1):
                        print(f"Vui lòng đợi {str(ll)} để đổi ip lần nữa        ", end="\r")
                        sleep(1)
        elif ':'in api_key:
            ipp, port, user, pas_ = api_key.split(":")
            ip = f"http://{user}:{pas_}@{ipp}:{port}"
            proxies = {"http": ip , "https": ip}
            return ip, proxies
        elif '-' in api_key:
            while True:
                try:
                    ip = requests.get(f"https://app.proxydt.com/api/public/proxy/get-new-proxy?license={api_key}&authen_ips={ip_me}", headers=headers).json()
                    print(ip)
                except Exception as e:
                    continue
                
                if ip["code"] == 1:
                    ipcc = ip['data']['http_ipv4']
                    proxies = {"http": ipcc , "https": ipcc}
                    return ipcc, proxies
                else:
                    if "Không tìm thấy license" in str(ip) or "Yêu cầu license key & whitelist Ip!" in str(ip) or 'Token không hợp lệ.' in str(ip):
                        print(ip)
                        return "KEYEXPIRED"
                    for ll in range(5, -1, -1):
                        print(f"Vui lòng đợi {str(ll)} để đổi ip lần nữa        ", end="\r")
                        sleep(1)
        elif len(api_key) == 32:
            datajs = {
            "api_key": api_key,
            "sign": "string",
            "id_location": 0
            }
            while True:
                try:
                    ip = requests.post(f"https://tmproxy.com/api/proxy/get-new-proxy", headers=headers, json=datajs).json()
                except Exception as e:
                    continue
                if ip['message'] == '':
                    ipcc = ip['data']['https']
                    ipcc = 'http://' + ipcc
                    proxies = {"http": ipcc , "https": ipcc}
                    return ipcc, proxies
                elif ip['message'] == 'API không tồn tại':
                    print("Key hết hạn hoặc không tồn tại!")
                    return
                else:
                    try:
                        timee = int(re.findall('\d+', ip['message'])[0]) # type: ignore
                        for ll in range(timee, -1, -1):
                            print(f"Vui lòng đợi {str(ll)} để đổi ip lần nữa        ", end="\r")
                            sleep(1)
                    except:
                        print(ip['message'])
        else:
            while True:
                try:
                    ip = requests.get(f"http://proxy.tinsoftsv.com/api/changeProxy.php?key={api_key}&location=0", headers=headers).json()
                except Exception as e:
                    continue
                if ip['success']:
                    ipcc = ip['proxy']
                    ipcc = 'http://' + ipcc
                    if 'null:' in ipcc:
                        continue
                    proxies = {"http": ipcc , "https": ipcc}
                    return ipcc, proxies
                else:
                    try:
                        timee = int(re.findall('\d+', ip['description'])[0]) # type: ignore
                        for ll in range(timee, -1, -1):
                            print(f"Vui lòng đợi {str(ll)} để đổi ip lần nữa        ", end="\r")
                            sleep(1)
                    except:
                        print(ip['description'])
                        print('Có key tinsoft lỗi!')
            