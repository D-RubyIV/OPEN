from queue import Queue
import threading
import base64
import re
import requests
import random
from time import sleep
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import fake_useragent, os
from selenium.webdriver.chrome.service import Service
from Moudule import ProxyWheel
from Moudule import CaptChaWheel
print("======================")
print("[1]: Tạo Tài Khoản")
print("[2]: Điểm danh")
print("======================")
CHOICE = int(input("NHẬP LỰA CHỌN: "))
FILE = "username.txt" if CHOICE == 1 else "account.txt"
class NetworkError(Exception):
    def __init__(self, message="This is a custom error."):
        self.message = message
        super().__init__(self.message)

def main(index, listDataMain, key):
    ipcc, proxies = ProxyWheel().getNewIp(api_key=key)
    
    user_agent = fake_useragent.FakeUserAgent(min_percentage=0.8).random
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{58962}")
    chrome_options.add_argument(f"--proxy-server={ipcc}")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("force-device-scale-factor=0.5")
    chrome_options.add_argument("high-dpi-support=0.5")
    # chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--lang=vi")
    chrome_options.add_argument("log-level=3")
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.set_window_size(600,1000)
    driver.set_window_position(500 * index, 0)

    action = ActionChains(driver)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://ty6699.com/m/")
        sleep(2)
        driver.refresh()
    except:
        print(f"[{index}] - Block IP")
        return
    
    for dataM in listDataMain:
        username, password, numberPhone ,fullName = map(str, dataM.split("|")[:4])
        if CHOICE == 1:
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Vui lòng nhập số điện thoại']"))).send_keys(numberPhone)
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Vui lòng nhập tên người dùng']"))).send_keys(username)
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Vui lòng nhập mật khẩu của bạn']"))).send_keys(password)
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Vui lòng xác nhận mật khẩu của bạn']"))).send_keys(password)
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Họ,tên thật(Phải điền)']"))).send_keys(fullName)
            wait.until(EC.presence_of_element_located((By.XPATH, "//button[span/text()='Tạo tài khoản']"))).click()
            sleep(3)
            open("account.txt", mode="a+", encoding="utf-8").write(f"{username}|{password}|{numberPhone}|{fullName}\n")
            print(f"ĐĂNG KÍ THÀNH CÔNG: {username}|{password}|{numberPhone}|{fullName}")
        else:
            wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Đăng nhập']"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Vui lòng nhập tên người dùng']"))).send_keys(username)
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Vui lòng nhập mật khẩu của bạn']"))).send_keys(password)
            wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='van-button van-button--default van-button--normal']"))).click()
            money = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'popup-close')]"))).click()
            money = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'cofre-box')]"))).click()
            money = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='lấy nó ngay bây giờ']"))).click()
            money = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'header-money-refresh')]"))).click()
            sleep(2)
            money = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'header-money')]/span"))).text
            open("reward.txt", mode="a+", encoding="utf-8").write(f"{username}|{password}|{numberPhone}|{fullName}|{money}\n")
            print(f"NHẬN THÀNH CÔNG: {username}|{password}|{numberPhone}|{fullName}|{money}")
        break
    driver.quit()
        
def do_stuff(jobs, index, keyProxy):
    while not jobs.empty():
        value = jobs.get()
        with open(FILE, 'w', encoding='utf-8') as f:
            for listData in jobs.queue:
                for data in listData:
                    username, password, numberPhone, fullName = map(str, data.split("|")[:4])
                    f.write(f"{username}|{password}|{numberPhone}|{fullName}\n")
        try:
            main(index, value, keyProxy)
        except NetworkError:
            print(F"{value} CAN'T CONNECT TO WEB")
        except Exception as e:
            if CHOICE == 1:
                open("errorRegister.txt", mode="a+", encoding="utf-8").write(f"{username}|{password}|{numberPhone}|{fullName}\n")
            if CHOICE == 2:
                open("errorReward.txt", mode="a+", encoding="utf-8").write(f"{username}|{password}|{numberPhone}|{fullName}\n")
            print(f"{value} LỖI")
        jobs.task_done()


if __name__ == "__main__":
    # Khởi tạo Queue
    jobs = Queue()
    KEYCAPTCHA = open("keycaptcha.txt", encoding="utf-8", mode="r").read().strip()
    listkeyProxy = [i.strip() for i in open("keyproxy.txt", "r", encoding="utf-8").readlines()]
    listDataAccount = open(FILE, encoding="utf-8", mode="r").readlines()

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