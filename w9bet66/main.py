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

print("[1] : NHẬN HỒNG BAO")
print("[2] : XỔ SỐ")
MODE = int(input("INPUT YOUR SELECT: "))

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
    global sode
    
    user_agent = fake_useragent.FakeUserAgent(min_percentage=0.8).random
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--proxy-server={ipcc}")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("force-device-scale-factor=0.5")
    chrome_options.add_argument("high-dpi-support=0.5")
    # chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--lang=vi")
    # chrome_options. add_argument('--blink-settings=imagesEnabled=false')
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.set_window_size(1200,1200)
    driver.set_window_position(500 * index, 0)

    action = ActionChains(driver)
    wait = WebDriverWait(driver, 40)
    wait20 = WebDriverWait(driver, 40)
    wait10 = WebDriverWait(driver, 10)
    wait15 = WebDriverWait(driver, 15)
    wait05 = WebDriverWait(driver, 5)
    wait02 = WebDriverWait(driver, 2)

    try:
        driver.get("https://w9bet66.com/")
        sleep(5)
    except:
        print(f"[{index}] - Block IP")
        raise NetworkError("Block IP")
    
    for dataM in listDataMain:
        wait20.until(EC.element_to_be_clickable((By.XPATH, "//div[@uib-modal-window='modal-window']")))
        username, password = map(str, dataM.split("|")[:2])
        print(username, password)
        closeModal(driver)
        wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='tài khoản']"))).send_keys(username.strip())
        wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='mật khẩu']"))).send_keys(password.strip())
        wait10.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@placeholder='Mã xác minh']")))[-1].click()
        sleep(3)
        statusSolveCaptcha = True
        for i in range(20):
            base64_img = wait10.until(EC.presence_of_all_elements_located((By.XPATH, "//img[@ng-class='$ctrl.styles.captcha']")))[-1].get_attribute("ng-src")
            print(f"[{index}] - Đợi giải captcha...")
            codeCaptcha = CaptChaWheel.sloveGPU(base64_img=base64_img, pathImg = f"Images/{key}.jpg")
            print(f"[{index}] - CaptCha Code: {codeCaptcha}")
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//input[@placeholder="Mã xác minh"]')))[-1].send_keys(str(codeCaptcha))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[span/text()="ĐĂNG NHẬP"]'))).click()
            sleep(2)
            if "chúc mừng bạn đã đăng ký thành công !" in driver.page_source:
                print(f"[{index}] - DANG KI THANH CONG")
                statusSolveCaptcha = True
                break
            elif "Lỗi mã xác minh" in str(driver.page_source) or "mã xác nhận không được bỏ trốn" in str(driver.page_source):
                wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary ng-scope"]'))).click()
                print(f"[{index}] - Lỗi mã xác minh")
                statusSolveCaptcha = False
            elif  "mã xác nhận không được bỏ trốn" in str(driver.page_source):
                wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary ng-scope"]'))).click()
                print(f"[{index}] - Mã xác nhận không được bỏ trống")
                statusSolveCaptcha = False
            elif "tài khoản sai định dạng" in str(driver.page_source):
                print(f"[{index}] - Tài khoản sai định dạng")
                return
            # elif "mật khẩu sai" in str(driver.page_source):
            #     print(f"[{index}] - Tài khoản mật khẩu sai")
            #     return
            elif "đã tồn tại" in str(driver.page_source):
                print(f"[{index}] - Đã tồn tại")
                return
            else:
                statusSolveCaptcha = True
                break
            sleep(2)
        if statusSolveCaptcha == False:
            print(f'[{index}] - Giải captcha không thành công')
            driver.quit()
            return
        

        # XONG LOGIN

        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@uib-modal-window='modal-window']")))
          
        for i in range(3):
            modalContent = wait20.until(EC.presence_of_element_located((By.XPATH, "//div[@class='modal-content']")))
            if "https" in modalContent.get_attribute('outerHTML'):
                break
            sleep(5)
        code = """
            document.querySelector('[class="modal-content"]').style.display = 'none';
        """
        driver.execute_script(code)     
                
        code = """
            var modalWindowElements = document.querySelectorAll('[uib-modal-window="modal-window"]');
            modalWindowElements.forEach(function(element) {
            element.style.display = 'none';
            });
        """
        driver.execute_script(code)
        

        if MODE == 1:
            print("GET GIFT CODE")
            arrayEle = None
            try:
                arrayEle = wait05.until(EC.presence_of_element_located((By.XPATH, '//div[text()="Hồng Bao May Mắn"]')))
            except:
                ()
            if arrayEle:
                print(f"[{index}] CÓ HỒNG BAO")
                arrayEle.click()
                arayElement = wait.until(EC.visibility_of_all_elements_located((By.XPATH, './/section[@class="row"]')))
                for element in arayElement:
                    wait.until(EC.element_to_be_clickable((By.XPATH, './/img'))).click()
                print(f"[{index}] ĐÃ NHẬN HỒNG BAO")
                with open("Response/DA_NHAN_HONG_BAO_THANH_CONG.txt", "a+", encoding="utf-8") as file:
                    file.write(f"{username}|{password}")
            else:
                print(f"[{index}] 0 CÓ HỒNG BAO")
            
        if MODE == 2:
            money = int(float(wait.until(EC.presence_of_element_located((By.XPATH, '//*[@title="Ví tài khoản"]'))).text))
            print(f'MONEY: {money}')
            if money == 0: 
                open("Response/ACC_HETTIEN.txt", encoding="utf-8", mode="a+").write(f"{username}|{password}\n")
                print(f"{username}|{password} Không đủ số dư !!!")
                driver.quit()
                return
            driver.get("https://w9bet66.com/Lobby/Lottery")
            sleep(2)
            closeModal(driver)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[span/text()="TP Xổ Số"]'))).click()
            sleep(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            driver.set_window_position(500 * index, 0)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Xổ Số Việt Nam"]'))).click()
            # print(wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[2]/div[2]/div[9]/div[7]"))))
            # element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Xổ Số Việt Nam-MIỀN BẮC']"))).click()
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[9]/div[7]/div[2]"))).click()
            countCuoc = money
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OKBtn']"))).click()
            driver.set_window_size(1200,1100)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="betBtn_x2 betBtnGroupActive"]')))[1].click()

            sode = getnumber()
            print(f'SO DE: {sode} - CUOC: {countCuoc}')
            
            wait.until(EC.presence_of_element_located((By.XPATH, f'//div[contains(@class, "mixBetBtnx3")][text()="{sode}"]'))).click()
            print(f"[{index}] CƯỢC: {countCuoc}")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait.until(EC.presence_of_element_located((By.XPATH, f'//div[contains(@class, "TicketCheckBtn")]'))).click()
            for value in str(money):
                wait.until(EC.presence_of_element_located((By.XPATH, f'//div[contains(@class, "keyboardNBBtn")][text()="{value}"]'))).click()
            sleep(1)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='keyboardOPBtn keyboardBtnBet']"))).click()
            for i in range(30):
                if "cược thành công" in str(driver.page_source):
                        print(f"{username}|{password} Đánh thành công, số: {sode}")
                        with open("Response/LICHSUDANH.txt", "a+", encoding="utf-8") as file:
                            file.write("%s|số đề: %s, số tiền: %s\n"%(f"{username}|{password}", sode, countCuoc))
                            break
                sleep(.2)

        sleep(1)
    driver.quit()
        
try:        
    with open("LICHSUDANH.txt", "r", encoding='utf-8') as f:
        sode = f.readlines()[-1].split("số đề: ")[1].split(", số")[0]
        sode = int(sode)
except:
    sode = 0        
        
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
   
def saveData(filename, value):
    for dataM in value:
        username, password = map(str, dataM.split("|")[:2])
        open(filename, encoding="utf-8", mode="a+").write(f"{username}|{password}\n")

    
def do_stuff(jobs, index, keyProxy):
    while not jobs.empty():
        value = jobs.get()
        with open('account.txt', 'w', encoding='utf-8') as f:
            for listData in jobs.queue:
                for data in listData:
                    
                    username, password = map(str, data.split("|")[:2])
                    f.write(f"{username}|{password}\n")
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
        sleep(1)
    jobs.join()