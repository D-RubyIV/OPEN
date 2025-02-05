from api.auth import login
from services import captcha
from utils import GenDevice 
from api.image import getImageBase64
from api.auth import Getinfo
import threading
import time
import json
import hashlib
import random

import queue

result_queue = queue.Queue()

def remove_invalid_characters(text):
   
    invalid_characters = ['Ä', 'Ă', 'Đ', 'Vá»', 'á»']
    for char in invalid_characters:
        text = text.replace(char, '')
    return text
# def read_accounts(file_name):
#     with open(file_name, "r", encoding='utf-8') as file:
#         accounts = []
#         for line in file:
#             parts = line.strip().split("|")
#             if len(parts) >= 2:
#                 username = parts[0]
#                 password = parts[1]
#                 username = remove_invalid_characters(username)
#                 password = remove_invalid_characters(password)
#                 accounts.append((username, password))
#         return list(set(tuple(account) for account in accounts))


def read_proxy_list(filename):
    with open(filename, 'r') as file:
        proxies = []
        for line in file:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                ip = parts[0]
                port = parts[1]
                username = parts[2]
                password = parts[3]
                proxies.append(f'http://{username}:{password}@{ip}:{port}')
        return proxies
def handle_callback(gold, chip, vip, dn, username, password, accessToken):
    return (username, password, gold, chip, vip, accessToken, "true")

def handle_account(account, proxy_list):
    username, password = account
    # print("Account => " + username + " => Password " + password)
    while True:
        captcha_result = getImageBase64.getCaptcha(proxy_list=proxy_list)
        if captcha_result is None:
            print("No captcha obtained. Retrying in 2 seconds...")
            time.sleep(2)
            continue

        if 'data' in captcha_result and 'image' in captcha_result['data']:
            captcha_image = captcha_result['data']['image']

        solver_result = captcha.createTask('CAP-E0650D69ACFD9F36B1E1954CC4EDE083', captcha_image)['solution']['text']

        deviceId = GenDevice.DeviceID(5)
        source = username + password + "4" + deviceId + "kUHH2za4EuRjWGPk"
        hash_value = hashlib.md5(source.encode()).hexdigest()
        hash_value = hash_value.lower()
        captcha_session_id = captcha_result['data']['sessionId']
        response = login.loginID(username, password, deviceId, hash_value, captcha_session_id, solver_result,proxy_list=proxy_list)
        if response == 'Retry':
            continue
        elif response == False:
            result_queue.put((username, password, "0", "0", "false", "null", "false"))
        else:
            info = response['data']['info']
            ipAddress = info['ipAddress']
            userId = info['userId']
            timestamp = info['timestamp']
            signature = response['data']['signature']
            accessToken = response['data']['accessToken']
            Getinfo.connect_and_listen(username, password, str(ipAddress), str(userId), int(timestamp), str(signature), lambda gold, chip, vip, dn: result_queue.put(handle_callback(gold, chip, vip, dn, username, password, accessToken)))
        break

def run(account): 

    file_name = 'account.txt'
    proxy_file = read_proxy_list('proxy.txt')
    handle_account(account,proxy_file)
    
    list_data = []
    while not result_queue.empty():
        result = result_queue.get()
        list_data.append(result)
    
    return list_data

