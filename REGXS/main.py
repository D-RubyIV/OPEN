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

class NetworkError(Exception):
    def __init__(self, message="This is a custom error."):
        self.message = message
        super().__init__(self.message)
        # 
        
def getnumber():
    path = "LICHSUDANH.txt"
    if os.path.exists(path):
        with open(path, "r", encoding='utf-8') as f:
            try:
                num = [i.strip() for i in f.readlines()]
                if "" in num: num.remove("")
                num = num[-1].split("số đề: ")[1].split(", số")[0]
                num = int(num)
                num += 1

                if len(str(num)) == 1:
                    num = "0" + str(num)
                elif num >= 100:
                    num = "00"
                else:
                    num = str(num)
                return(str(num))
            except:
                return "00"
    else:
        return "00"


def main(index, listDataMain, key):
    # ipcc, proxies = ProxyWheel().getNewIp(api_key=key)
    
    user_agent = fake_useragent.FakeUserAgent(min_percentage=0.8).random
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{58962}")
    # chrome_options.add_argument(f"--proxy-server={ipcc}")
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
    wait = WebDriverWait(driver, 40)
    wait20 = WebDriverWait(driver, 40)
    wait10 = WebDriverWait(driver, 40)
    wait05 = WebDriverWait(driver, 5)
    wait02 = WebDriverWait(driver, 2)

    try:
        driver.get("https://www.nbvn777.com/m/home?fbclid=IwAR09hYp01buVJbxEvA7WvbSg9JiflV8nb31dNtljyI6A-gxS08GOoHr6v4k_aem_AfdFai2SuV2eXNq2x9tFF_YqkWWc_a1bYR-8IykBEAVQS4rb65mLb_B0cZzcGAXBwFlz3pZfoNyB4g8-vl-6DeJV")
        sleep(2)
        driver.refresh()
    except:
        print(f"[{index}] - Block IP")
        return
    
    for dataM in listDataMain:
        username, password, fullName, birthDay, city, bankCode, nameBank, passBank, phone = map(str, dataM.split("|")[:9])
        print(username, password, fullName, birthDay, city, bankCode, nameBank, passBank, phone)
        
        if '<div class="popup_title">vip</div>' in str(driver.page_source):
            wait10.until(EC.presence_of_element_located((By.XPATH, "//div[@class='am-navbar-title close-btn']"))).click()

        wait10.until(EC.presence_of_element_located((By.XPATH, "//span[@class='btn-register']"))).click()
        wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Nhập tên đăng nhập *']"))).send_keys(username)
        wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Mật khẩu *']"))).send_keys(password)
        wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Xác nhận lại mật khẩu *']"))).send_keys(password)
        wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Số điện thoại ']"))).send_keys(phone)

        while "Mã xác nhận *" in str(driver.page_source):
            eleCaptcha = wait10.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='captcha']")))
            codeCaptCha = str(CaptChaWheel.sloveGPU(base64_img=eleCaptcha.get_attribute("src"), pathImg=f"Images/{index}_img.png")).replace("-","").replace(".","").replace(",","").replace(" ","")
            print(codeCaptCha)
            wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Mã xác nhận *']"))).send_keys(codeCaptCha)
            wait10.until(EC.presence_of_element_located((By.XPATH, "//button[@class='submit-btn register-btn']"))).click()
            sleep(3)
            if '<a class="am-modal-button" role="button">Xác nhận</a>' in str(driver.page_source):
                wait10.until(EC.presence_of_element_located((By.XPATH, "//div[@class='am-modal-button-group-v am-modal-button-group-normal']"))).click()
            if 'Vui lòng đợi' in str(driver.page_source):     
                print("Vui lòng đợi")
                break 
        sleep(3)
        driver.refresh()
        eles = wait10.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'game-menu-item') and contains(span/text(),'Xổ Số')]"))).click()
        wait10.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='vendor-item']")))[0].click()
        while True:
            # if driver.execute_script("return document.readyState") == "complete":
            #     break
            print(driver.title)
            if driver.title == "Play Game Online":
                break
            time.sleep(2)
        print("DONE LOAD")
        wait10.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='lobby-item isSale']")))[0].click()
        so_chon = getnumber()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='TÌM SỐ']"))).send_keys(so_chon)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='query-submit ']"))).click()
        countMoney = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='money-box']"))).find_element(By.XPATH,"div[1]").text
        if (int(float(countMoney)) == 0):
            print("KHONG CO TIEN")
            driver.quit()
            return
        for i in range(int(float(countMoney))-1):
            wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='sc-plus']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='submit-btn btn']"))).click()
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'submit-btn') and contains(@class, 'btn') and text()='Xác nhận']"))).click()
        sleep(5)
        with open("LICHSUDANH.txt", "a+", encoding="utf-8") as file:
            file.write("%s|số đề: %s, số tiền: %s\n"%(f"{username}|{password}|{fullName}|{birthDay}|{city}|{bankCode}|{nameBank}|{passBank}|{phone}", so_chon, countMoney))
        break            
    driver.quit()
        
try:        
    with open("LICHSUDANH.txt", "r", encoding='utf-8') as f:
        sode = f.readlines()[-1].split("số đề: ")[1].split(", số")[0]
        sode = int(sode)
except:
    sode = 0        
        
def do_stuff(jobs, index, keyProxy):
    while not jobs.empty():
        value = jobs.get()
        with open('username.txt', 'w', encoding='utf-8') as f:
            for listData in jobs.queue:
                for data in listData:
                    
                    username, password, fullName, birthDay, city, bankCode, nameBank, passBank, phone = map(str, data.split("|")[:9])
                    f.write(f"{username}|{password}|{fullName}|{birthDay}|{city}|{bankCode}|{nameBank}|{passBank}|{phone}\n")
        try:
            main(index, value, keyProxy)
        except NetworkError:
            print(F"{value} CAN'T CONNECT TO WEB")
        # except Exception as e:
        #     print(f"{value} LỖI")
        jobs.task_done()


if __name__ == "__main__":
    # Khởi tạo Queue
    jobs = Queue()
    KEYCAPTCHA = open("keycaptcha.txt", encoding="utf-8", mode="r").read().strip()
    listkeyProxy = [i.strip() for i in open("keyproxy.txt", "r", encoding="utf-8").readlines()]
    listDataAccount = open("username.txt", encoding="utf-8", mode="r").readlines()

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