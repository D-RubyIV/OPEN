import json
from queue import Queue
import threading
import base64
import re
import requests
import random
import hashlib, cloudscraper
import random
import string
from time import sleep
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import fake_useragent
import os
from Moudule import ProxyWheel
from Moudule import CaptChaWheel
from selenium.webdriver.chrome.service import Service

class NetworkError(Exception):
    def __init__(self, message="This is a custom error."):
        self.message = message
        super().__init__(self.message)


def getnumber():
    path = "Response/LICHSUDANH.txt"
    if os.path.exists(path):
        with open(path, "r", encoding='utf-8') as f:
            try:
                num = [i.strip() for i in f.readlines()]
                if "" in num:
                    num.remove("")
                num = num[-1].split("số đề: ")[1].split(", số")[0]
                num = int(num)
                num += 1

                if len(str(num)) == 1:
                    num = "0" + str(num)
                elif num >= 100:
                    num = "00"
                else:
                    num = str(num)
                return (str(num))
            except:
                return "00"
    else:
        return "00"


def main(index, listDataMain, key):
    for data in listDataMain:
        username, password = str(data).split("|")[:2]
        # ipString, proxies = ProxyWheel().getNewIp(api_key=key)
        ua = fake_useragent.UserAgent(min_percentage=0.9)
        # CHROME SETTING
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("force-device-scale-factor=0.65")
        options.add_argument("high-dpi-support=0.65")
        # options.add_argument("--disable-notifications")
        # options.add_argument("--disable-infobars")
        # options.add_argument("--disable-extensions")
        # options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("detach", True)
        # options.add_argument('--proxy-server=http://{}:{}'.format(PROXY_IP, PROXY_PORT))
        driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
        driver.set_window_position(300*index, 0)
        driver.set_window_size(600, 800)

        # LOGIN
        driver.get("https://w9bet66.com/")
        
  
    



def do_stuff(jobs, index, keyProxy):
    while not jobs.empty():
        value = jobs.get()
        with open('username.txt', 'w', encoding='utf-8') as f:
            for listData in jobs.queue:
                for data in listData:

                    username, password, fullName, birthDay, city, bankCode, nameBank, passBank, = map(str, data.split("|")[:8])
                    f.write(f"{username}|{password}|{fullName}|{birthDay}|{city}|{bankCode}|{nameBank}|{passBank}\n")
        try:
            main(index, value, keyProxy)
        except NetworkError:
            print(F"{value} CAN'T CONNECT TO WEB")
        # except Exception as e:
        #     print(f"{value} LỖI")
        jobs.task_done()


if __name__ == "__main__":
    jobs = Queue()
    KEYCAPTCHA = open("keycaptcha.txt", encoding="utf-8", mode="r").read().strip()
    listkeyProxy = [i.strip() for i in open("keyproxy.txt", "r", encoding="utf-8").readlines()]
    listDataAccount = open("account.txt", encoding="utf-8", mode="r").readlines()

    dataGet = []
    row = 0
    for dataAccount in listDataAccount:
        dataGet.append(dataAccount.strip())
        if len(dataGet) >= 1:
            jobs.put(dataGet.copy())
            dataGet.clear()
    jobs.put(dataGet.copy())
    dataGet.clear()
    print("Đang Chuẩn Bị Chạy:", jobs.qsize(), "Tài Khoản!")

    for index in range(len(listkeyProxy)):
        sleep(index * 5)
        print(f"Luồng {index}: Bắt đầu tạo chạy!")
        key = listkeyProxy[index]
        worker = threading.Thread(
            target=do_stuff,
            args=(
                jobs,
                index,
                key,
            ),
        )
        worker.start()
        sleep(5)
    jobs.join()
