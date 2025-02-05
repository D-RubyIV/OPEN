import requests
import random

def getCaptcha(proxy_list=None):
    try:
        proxy = random.choice(proxy_list) if proxy_list else None
        proxies_dict = {'http': proxy, 'https': proxy} if proxy else None

        if proxy:
            response = requests.get('https://api.azhkthg1.net/id?command=getCaptcha&sessionId=', proxies=proxies_dict)
        else:
            response = requests.get('https://api.azhkthg1.net/id?command=getCaptcha&sessionId=')
        #print(response.text)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        return None
