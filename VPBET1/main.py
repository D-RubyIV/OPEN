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



def closeModal(driver):
    wait20 = WebDriverWait(driver, 20)
    wait40 = WebDriverWait(driver, 40)
    wait40.until(EC.visibility_of_element_located((By.XPATH, "//div[@uib-modal-window='modal-window']")))
    wait40.until(EC.visibility_of_element_located((By.XPATH, "//div[@uib-modal-backdrop='modal-backdrop']")))
    for i in range(3):
        modalContent = wait20.until(EC.presence_of_element_located((By.XPATH, "//div[@class='modal-content']")))
        if "https" in modalContent.get_attribute('outerHTML'):
            break
        sleep(5)
            
    code = """
        var modalWindowElements = document.querySelectorAll('[uib-modal-window="modal-window"]');
        modalWindowElements.forEach(function(element) {
        element.style.display = 'none';
        });
    """
    driver.execute_script(code)
    code = """
        document.querySelector('[uib-modal-backdrop="modal-backdrop"]').style.display = 'none';
    """
    driver.execute_script(code)


def main(index, listDataMain, key):
    ipcc, proxies = ProxyWheel().getNewIp(api_key=key)
    
    user_agent = fake_useragent.FakeUserAgent(min_percentage=0.8).random
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--proxy-server={ipcc}")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("force-device-scale-factor=0.5")
    chrome_options.add_argument("high-dpi-support=0.5")
    # chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--lang=en")
    # chrome_options. add_argument('--blink-settings=imagesEnabled=false')
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.set_window_size(1400,1200)
    driver.set_window_position(500 * index, 0)

    action = ActionChains(driver)
    wait40 = WebDriverWait(driver, 40)
    wait20 = WebDriverWait(driver, 40)
    wait10 = WebDriverWait(driver, 10)
    wait15 = WebDriverWait(driver, 15)
    wait05 = WebDriverWait(driver, 5)
    wait02 = WebDriverWait(driver, 2)

    for dataM in listDataMain:
        print(dataM)
        username, password, fullName, numberPhone, numberBank, passBank = map(str, dataM.split("|")[:6])
        try:
            driver.get("https://vpbet1.com?c=vMPEx39")
            sleep(5)
        except:
            print(f"[{index}] - Block IP")
            raise NetworkError("Block IP")
        wait40.until(EC.presence_of_element_located((By.XPATH, "//div[@class='q-dialog fullscreen no-pointer-events q-dialog--modal free-spin-wheel-modal']")))
        code = """
            document.querySelector('[class="q-dialog fullscreen no-pointer-events q-dialog--modal free-spin-wheel-modal"]').style.display = 'none';
        """
        driver.execute_script(code)
        wait40.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Register']"))).click()
        wait10.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@class='q-field__native q-placeholder']")))[0].send_keys(numberPhone.strip())
        wait10.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@class='q-field__native q-placeholder']")))[1].send_keys(username.strip())
        wait10.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@class='q-field__native q-placeholder']")))[2].send_keys(password.strip())
        wait10.until(EC.presence_of_element_located((By.XPATH, "//button[span/text()='Play Now']"))).click()

        sleep(5)
        if str(driver.current_url) == "https://vpbet1.com/casino/home":
            print(f"[{index}] REG THÀNH CÔNG")
            sleep(100)
            with open("account.txt", "a+", encoding="utf-8") as file:
                file.write(f"{username}|{password}|{fullName}|{numberPhone}|{numberBank}|{passBank}\n")
            break
        else:
            print(f"[{index}] REG THẤT BẠI")
        driver.quit()

def image_url_to_base64(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check for any errors during the request
        base64_image = base64.b64encode(response.content).decode('utf-8')
        return base64_image
    except Exception as e:
        print(f"Error: {e}")
        return None

def do_stuff(jobs, index, keyProxy):
    while not jobs.empty():
        value = jobs.get()
        with open('username.txt', 'w', encoding='utf-8') as f:
            for listData in jobs.queue:
                for data in listData:
                    username, password, fullName, numberPhone, numberBank, passBank = map(str, data.split("|")[:6])
                    f.write(f"{username}|{password}|{fullName}|{numberPhone}|{numberBank}|{passBank}\n")
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
        sleep(1)
    jobs.join()