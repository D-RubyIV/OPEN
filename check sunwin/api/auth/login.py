import requests,json
import random
def loginID(username,password,deviceID,hash,sessionID,answer,proxy_list=None):
    url = "https://api.azhkthg1.net/id"

    payload = json.dumps({
        "command": "loginWebHash",
        "username": username,
        "password": password,
        "platformId": 4,
        "advId": "",
        "deviceId": deviceID,
        "hash": hash,
        "brand": "sun.win",
        "sessionId": sessionID,
        "answer": answer
    })
    
    headers = {
        'Host': 'api.azhkthg1.net',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'https://web.sun20.win',
        'Referer': 'https://web.sun20.win',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    proxy = random.choice(proxy_list) if proxy_list else None
    proxies_dict = {'http': proxy, 'https': proxy} if proxy else None
    response = requests.request("POST", url, headers=headers, data=payload,proxies=proxies_dict)
    try:
        json_response = response.json()
    except:
        return None
    
    status = json_response.get('status', None)
    
    if status == 0:
        return json_response
    elif status == 702:
        return "Retry"
    elif status == 703:
        return "Session Die"
    else: 
        return False

