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
    path = "Response/LICHSUDANH.txt"
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
    wait = WebDriverWait(driver, 40)
    wait20 = WebDriverWait(driver, 40)
    wait10 = WebDriverWait(driver, 40)
    wait05 = WebDriverWait(driver, 5)
    wait02 = WebDriverWait(driver, 2)

    try:
        driver.get("https://win939d.com/home/game?currency=VND&cid=272084&gameCategoryId=0")
        sleep(2)
        driver.refresh()
    except:
        print(f"[{index}] - Block IP")
        return
    
    for dataM in listDataMain:
        username, password, fullName, birthDay, city, bankCode, nameBank, passBank = map(str, dataM.split("|")[:8])
        print(username, password, fullName, birthDay, city, bankCode, nameBank, passBank)
        wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Tên Tài Khoản']"))).send_keys(username)
        wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Mật Khẩu']"))).send_keys(password)
        wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Vui lòng xác nhận lại mật khẩu !']"))).send_keys(password)
        wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Họ Tên Thật']"))).send_keys(fullName)
        wait10.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "ant-btn ant-btn-primary ant-btn-block") and contains(span/text(), "ĐĂNG KÝ")]'))).click()
        while True:
            a = driver.execute_script("return document.readyState")
            if a == "complete":
                break
            time.sleep(2)
        sleep(10)
        validCaptcha = False
        for i in range(20):
            if "Chọn hình ảnh với" in str(driver.page_source):
                print(f"CAPTCHA CHỌN ẢNH")
                wait10.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'geetest_close')]"))).click()
                wait10.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "ant-btn ant-btn-primary ant-btn-block") and contains(span/text(), "ĐĂNG KÝ")]'))).click()
                sleep(5)
            elif "Trượt để hoàn thành trò đố" in str(driver.page_source):
                print(f"CAPTCHA KÉO ẢNH")
                validCaptcha = True
                element = wait10.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "geetest_bg")]')))
                # element = wait10.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Hình ảnh 4 / 6."]')))
                url = (
                    str(element.get_attribute("style"))
                    .split('url("')[1]
                    .split('");')[0]
                )
                print(f"[{index}]URL: {url}")
                base64_code = driver.execute_script(
                    """
                const getBase64FromUrl = async (url) => {
                    const data = await fetch(url);
                    const blob = await data.blob();
                    return new Promise((resolve) => {
                        const reader = new FileReader();
                        reader.readAsDataURL(blob); 
                        reader.onloadend = () => {
                            const base64data = reader.result;   
                            resolve(base64data);
                        }
                    });
                }
                return getBase64FromUrl(arguments[0]).then(function(base64data) {
                    return base64data.split(";base64,")[1];
                });
                """,
                    url,
                )
                payload = {
                    "key": "7ce6508ade8e87d51a091d78b82f5616",
                    "method": "base64",
                    "textinstructions": "Slider",
                    "click": "geetest",
                    "body": base64_code,
                }
                result = requests.post("http://api.cap.guru/in.php", data=payload)
                print(
                    f"[{index}]{result.text}"
                )  # OK|0a58745a28468e29ad7d533e897ee764|36db28fdeacd0b857a6f77625b196be4|ed7a85beb9856075a5e495cb63c944d72be3cc758a83dcef511b7b32abb97bbcb0ad9d0137014c378b56
                if "|" not in result.text:
                    return
                while True:
                    time.sleep(3)
                    rt = result.text.split("|")
                    url = "http://api.cap.guru/res.php?key=7ce6508ade8e87d51a091d78b82f5616&id=" + rt[1]
                    response = requests.get(url=url, timeout=10)
                    print(
                        f"[{index}]{response.text}"
                    ) 
                    if "OK" in response.text:
                        print(response.text)
                        break
                    
                coorX = int(str(response.text).split("x=")[1].split(",y=")[0])
                print(f'COOR: {coorX}')
                
                action = ActionChains(driver)
                element = wait10.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "geetest_arrow geetest_arrow_1")]')))
                print(element)
                el = action.move_to_element(element).click_and_hold().move_by_offset(coorX-6, 0).release().perform()
                print("DONE")
                sleep(6)
            if "Mẹo" in str(driver.page_source):
                break
            
            
        
            
        # SET PASS BANK
        driver.get("https://win939d.com/home/withdraw?current=3")
        print(passBank)
        wait10.until(EC.presence_of_all_elements_located((By.XPATH, '//input[@type="number"]')))[0].send_keys(passBank)
        sleep(1)
        wait10.until(EC.presence_of_all_elements_located((By.XPATH, '//input[@type="number"]')))[1].send_keys(passBank)
        wait10.until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "ant-btn ant-btn-primary")]'))).click()
        sleep(5)

        driver.get("https://win939d.com/home/withdraw?current=3")
        wait10.until(EC.presence_of_element_located((By.XPATH, '//div[a/text()="Thêm tài khoản ngân hàng mới"]'))).click()
        wait10.until(EC.presence_of_element_located((By.XPATH, '//input[@type="number"]'))).send_keys(passBank)
        wait10.until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "ant-btn ant-btn-primary")]'))).click()
        wait10.until(EC.presence_of_element_located((By.XPATH, '//div[@class="ant-select-selection ant-select-selection--single"]'))).click()
        wait10.until(EC.presence_of_element_located((By.XPATH, '//li[@name="VPBANK"]')))
        sleep(1)
        wait10.until(EC.presence_of_element_located((By.XPATH, '//li[@name="VPBANK"]'))).click()
        wait10.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Vui lòng nhập số tài khoản ngân hàng"]'))).send_keys(bankCode)
        wait10.until(EC.presence_of_all_elements_located((By.XPATH, '//button[contains(@class, "ant-btn ant-btn-primary")]')))[1].click()
        sleep(5)
        
        
        driver.get("https://win939d.com/home/event?gameCategoryId=0&tabItem=discount")
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"event-category-container-item")]')))[0].click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class,"ant-btn ant-btn-success")]'))).click()
        sleep(5)
        open("account.txt", mode="a+", encoding="utf-8").write(f"{username}|{password}|{bankCode}|{passBank}|\n")
        print(f"ĐĂNG KÍ THÀNH CÔNG: {username}|{password}|{bankCode}|{passBank}")
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
                    
                    username, password, fullName, birthDay, city, bankCode, nameBank, passBank, = map(str, data.split("|")[:8])
                    f.write(f"{username}|{password}|{fullName}|{birthDay}|{city}|{bankCode}|{nameBank}|{passBank}\n")
        try:
            main(index, value, keyProxy)
        except NetworkError:
            print(F"{value} CAN'T CONNECT TO WEB")
        except Exception as e:
            print(f"{value} LỖI")
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