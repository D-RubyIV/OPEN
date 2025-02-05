from collections import deque
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
from selenium.common.exceptions import *
import fake_useragent, os
from colorama import init, Fore, Back, Style
from pymailtm.pymailtm import MailTm

global MYPROXY, MYCOUNTTHREAD, MYRUNNINGCHROME, CHANGINGIP
MYPROXY = None
CHANGINGIP = False
RUNNINGCHROME = {}

FG = Fore.GREEN
FR = Fore.RED
FY = Fore.YELLOW
FW = Fore.WHITE

from Moudule import ProxyWheel
from Moudule import CaptChaWheel

def getNewIp(api_key):
    global MYPROXY
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    if str(api_key).count("-") == 5:
        while True:
            listProvine = [
                i["id"]
                for i in requests.get(
                    "https://wwproxy.com/api/client/province?search_text="
                ).json()["data"]
            ]
            ip = requests.get(
                f"https://wwproxy.com/api/client/proxy/available?key={api_key}&provinceId={random.choice(listProvine)}"
            ).json()
            print(ip)
            if ip["errorCode"] == 0:
                ipcc = ip["data"]["proxy"]
                proxies = {"http": ipcc, "https": ipcc}
                MYPROXY = ipcc
                return ipcc, proxies
            elif ip["errorCode"] == 1:
                for ll in range(20, -1, -1):
                    print(f"Vui lòng đợi {str(ll)} để đổi ip lần nữa        ", end="\r")
                    sleep(1)

    elif len(api_key) == 32:
        datajs = {"api_key": api_key, "sign": "string", "id_location": 0}
        while True:
            try:
                ip = requests.post(
                    f"https://tmproxy.com/api/proxy/get-new-proxy",
                    headers=headers,
                    json=datajs,
                ).json()
            except Exception as e:
                continue
            if ip["message"] == "":
                ipcc = ip["data"]["https"]
                ipcc = "http://" + ipcc
                proxies = {"http": ipcc, "https": ipcc}
                return ipcc, proxies
            elif ip["message"] == "API không tồn tại":
                print("Key hết hạn hoặc không tồn tại!")
                return
            else:
                try:
                    timee = int(re.findall("\d+", ip["message"])[0])  # type: ignore
                    for ll in range(timee, -1, -1):
                        print(
                            f"Vui lòng đợi {str(ll)} để đổi ip lần nữa        ",
                            end="\r",
                        )
                        sleep(1)
                except:
                    print(ip["message"])


class NetworkError(Exception):
    def __init__(self, message="This is a custom error."):
        self.message = message
        super().__init__(self.message)


def getnumber():
    path = "Response/LICHSUDANH.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            num = f.readlines()[-1].split("Số Đề: ")[1].split(", Số")[0]
            num = int(num)
            num += 1

            if len(str(num)) == 1:
                num = "0" + str(num)
            elif num >= 100:
                num = "00"
            else:
                num = str(num)
            return str(num)
    else:
        return "00"


def refreshMail(mail, status: int):
    endMail = "@" + mail.split("@")[1].split(":")[0]
    if not os.path.exists("SUCCESS.txt"):
        open("SUCCESS.txt", encoding="utf-8", mode="w")
    if not os.path.exists("FAILURE.txt"):
        open("FAILURE.txt", encoding="utf-8", mode="w")

    if status == 0:
        with open("SUCCESS.txt", encoding="utf-8", mode="a+") as file:
            file.write(f"{endMail}\n")

        with open("SUCCESS.txt", encoding="utf-8", mode="r") as file:
            MAILSUCESS = [i.strip() for i in file.readlines()]

        MAILSUCESS = list(set(MAILSUCESS) - {""})
        open("SUCCESS.txt", encoding="utf-8", mode="w")
        with open("SUCCESS.txt", encoding="utf-8", mode="a+") as file:
            for i in MAILSUCESS:
                file.write(f"{i}\n")

        with open("EDUACCOUNT.txt", encoding="utf-8", mode="r") as edu_file:
            MAILOK = [i.strip() for i in edu_file.readlines() if endMail in i]

        if os.path.exists(f"SUCCESS/{endMail}.txt"):
            MAILOK += [
                i.strip()
                for i in open(
                    f"SUCCESS/{endMail}.txt", encoding="utf-8", mode="r"
                ).readlines()
            ]

        with open(f"SUCCESS/{endMail}.txt", encoding="utf-8", mode="w") as edu_file:
            edu_file.write("\n".join(MAILOK))

    if status == 1:
        with open("FAILURE.txt", encoding="utf-8", mode="a+") as file:
            file.write(f"{endMail}\n")

        with open("FAILURE.txt", encoding="utf-8", mode="r") as file:
            MAILFAILURE = [i.strip() for i in file.readlines()]

        MAILFAILURE = list(set(MAILFAILURE) - {""})
        open("FAILURE.txt", encoding="utf-8", mode="w")
        with open("FAILURE.txt", encoding="utf-8", mode="a+") as file:
            for i in MAILFAILURE:
                file.write(f"{i}\n")

    with open("EDUACCOUNT.txt", encoding="utf-8", mode="r") as edu_file:
        MAILNOTOK = [i.strip() for i in edu_file.readlines() if endMail not in i]

    MAILNOTOK = list(set(MAILNOTOK) - {""})

    with open("EDUACCOUNT.txt", encoding="utf-8", mode="w") as edu_file:
        edu_file.write("\n".join(MAILNOTOK))


def fillInfo(driver):
    print("FILL")
    driver.switch_to.default_content()
    wait40 = WebDriverWait(driver, 40)
    wait10 = WebDriverWait(driver, 10)
    wait05 = WebDriverWait(driver, 5)
    wait02 = WebDriverWait(driver, 2)
    wait40.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Type in a school name"]')
        )
    )
    driver.execute_script(
        "arguments[0].scrollIntoView(true);",
        wait40.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//input[@id="sse-vnext-email-input"]')
            )
        ),
    )

    day = str(random.randint(1, 28))
    month = str(random.randint(1, 12))
    year = str(random.randint(2006, 2011))
    randomDateTime = day if len(day) == 2 else f"0{day}"
    randomDateTime += month if len(month) == 2 else f"0{month}"
    randomDateTime += year

    wait40.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//input[@id="sse-vnext-dob-input"]')
        )
    ).send_keys(randomDateTime)
    # wait40.until(EC.visibility_of_element_located((By.XPATH,  '//input[@id="sse-vnext-email-input"]'))).send_keys(str(mailQueue.get()).split(":")[0])

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.switch_to.frame(
        wait40.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "iframe[aria-label='Verification challenge']",
                )
            )
        )
    )
    print(f"[{index}]Switch OK1")
    driver.switch_to.frame(
        wait40.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//iframe[@class='game-core-frame']")
            )
        )
    )
    print(f"[{index}]Switch OK2")
    wait40.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//p[text()='Hãy giải câu đố để chúng tôi biết bạn không phải là robot.']",
            )
        )
    )
    wait40.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[text()='Tiếp theo']")
        )
    )
    sleep(3)
    wait40.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[text()='Tiếp theo']")
        )
    ).click()
    sleep(5)
    while "Chọn một hình vuông hiển thị hai vật thể giống nhau." in str(
        driver.page_source
    ):
        if "Xác minh hoàn tất!" in str(driver.page_source):
            print(f"[{index}]Xác minh hoàn tất!")
            break
        element = wait10.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'button[aria-label="Hình ảnh 4 / 6."]')
            )
        )
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
        # print(base64_code)
        payload = {
            "textinstructions": "Pick one square that shows two identical objects",
            "click": "funcap",
            "key": "9b7f0385b4b472b6bfb28e491d83c48f",
            "method": "base64",
            "body": base64_code,
        }
        resoult = requests.post("http://api.cap.guru/in.php", data=payload)
        print(
            f"[{index}]{resoult.text}"
        )  # OK|0a58745a28468e29ad7d533e897ee764|36db28fdeacd0b857a6f77625b196be4|ed7a85beb9856075a5e495cb63c944d72be3cc758a83dcef511b7b32abb97bbcb0ad9d0137014c378b56
        if "|" not in resoult.text:
            return
        while True:
            time.sleep(3)
            rt = resoult.text.split("|")
            url = (
                "http://api.cap.guru/res.php?key=9b7f0385b4b472b6bfb28e491d83c48f&id="
                + rt[1]
            )
            response = requests.get(url=url, timeout=10)
            print(
                f"[{index}]{response.text}"
            )  # OK|3 - số 3 là thứ tự ảnh kết quả (tính từ 1)
            if "OK" in response.text:
                print(f"[{index}]CLICK CAPTCHA")

                pattern = r"x=(\d+),y=(\d+)"

                # Using re.search to find the pattern in the text
                match = re.search(pattern, response.text)

                if match:
                    x_value = int(match.group(1))  # Extracting x value
                    y_value = int(match.group(2))  # Extracting y value
                    # print("x =", x_value)
                    # print("y =", y_value)
                    # x_value = 50
                    # y_value = 150

                    # x_cor = (x_value - 50) / 100 + 1
                    # y_cor = (y_value - 50) / 100 + 1

                    # indexClick = x_cor * y_cor

                    # indexClick = (x_value/50 + 1) * (y_value/50)
                else:
                    print("Coordinates not found in the text.")
                ac = ActionChains(driver)
                elem = wait10.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//div[contains(@class, "challenge-container")]',
                        )
                    )
                )
                # ac.move_to_element_with_offset(elem, 0, 0)
                # ac.move_to_element(elem).move_by_offset(
                #     x_value, y_value
                # ).click().perform()
                # x 50 y 50 -> 1
                # x 150 y 50 -> 2
                # x 250 y 50 -> 3
                # x 250 y 150 -> 6
                if (x_value == 50 and y_value == 50):
                    # print("1")
                    indexClick = 1
                elif (x_value == 150 and y_value == 50):
                    # print("2")
                    indexClick = 2
                elif (x_value == 250 and y_value == 50):
                    # print("3")
                    indexClick = 3
                elif (x_value == 50 and y_value == 150):
                    # print("4")
                    indexClick = 4
                elif (x_value == 150 and y_value == 150):
                    # print("5")
                    indexClick = 5
                elif (x_value == 250 and y_value == 150):
                    # print("6")
                    indexClick = 6

                # result = response.text.split("|")[1]
                wait40.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            f'//div[contains(@class, "challenge-container")]//button[{indexClick}]',
                        )
                    )
                ).click()
                break
            if "ERROR_CAPTCHA_UNSOLVABLE" in response.text:
                print(f"[{index}]ERROR_CAPTCHA_UNSOLVABLE")
                wait10.until(
                    EC.element_to_be_clickable(
                        (
                            By.CSS_SELECTOR,
                            'button[aria-label="Bắt đầu lại"]',
                        )
                    )
                ).click()
                wait40.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//button[text()='Tiếp theo']")
                    )
                )
                sleep(3)
                wait40.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//button[text()='Tiếp theo']")
                    )
                ).click()
                sleep(4)
                break
        sleep(5)

def main(index, listDataMain, key):
    global RUNNINGCHROME, MYCOUNTTHREAD, MYPROXY, CHANGINGIP

    while True:
        # (Nếu ko có profile nào chạy hoặc chưa chạy profile nào) và  đổi ip đang là False
        if (
            sum(value is False for value in RUNNINGCHROME.values()) == MYCOUNTTHREAD
            or len(RUNNINGCHROME.keys()) == 0
        ) and CHANGINGIP == False:
            CHANGINGIP = True
            print("ĐANG CHANGE IP")
            RUNNINGCHROME.clear()
            ProxyString, ipcc = getNewIp(api_key=key)
            print(f"[{index}]{FG} CHANGE IP: {ProxyString}{FW}")
            CHANGINGIP = False
            RUNNINGCHROME[index] = True
            break
        #  Nếu đang đổi ip
        elif CHANGINGIP == True:
            print(f"Đợi đổi proxy hoàn tất {RUNNINGCHROME}")
            sleep(1)
            continue
        # Nếu số profile key nhỏ hơn số luồng
        elif len(RUNNINGCHROME.keys()) < MYCOUNTTHREAD:
            RUNNINGCHROME[index] = True
            break
        # Nếu số profile đang chạy lớn hơn 0 và số profile key = số luồng
        elif (
            sum(value is True for value in RUNNINGCHROME.values()) > 0
            and len(RUNNINGCHROME.keys()) == MYCOUNTTHREAD
        ):
            print(f"WAIT {RUNNINGCHROME}")
            sleep(2)
        else:
            print(f"SLEEP {RUNNINGCHROME}")
            sleep(2)

    print(f"[{index}]{FG} CONNECT IP: {MYPROXY}{FW}")

    try:
        # ipcc, proxies = ProxyWheel().getNewIp(api_key=key)
        MAILTM = MailTm()
        user_agent = fake_useragent.FakeUserAgent(min_percentage=0.8).random
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument(f"--proxy-server={MYPROXY}")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("force-device-scale-factor=0.65")
        chrome_options.add_argument("high-dpi-support=0.65")
        # chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--lang=vi")
        chrome_options.add_argument("log-level=3")
        # chrome_options. add_argument('--blink-settings=imagesEnabled=false')
        # chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(40)
        driver.set_window_size(500, 800)
        driver.set_window_position(500 * index, 0)

        action = ActionChains(driver)
        wait40 = WebDriverWait(driver, 40)
        wait10 = WebDriverWait(driver, 10)
        wait05 = WebDriverWait(driver, 5)
        wait02 = WebDriverWait(driver, 2)

        try:

            driver.get("https://signup.azure.com/studentverification?offerType=1")
            sleep(2)
            driver.refresh()
        except:
            RUNNINGCHROME[index] = False
            driver.quit()

            raise NetworkError("Block IP")

        for dataM in listDataMain:
            print(f"[{index}]|{dataM}")
            username, password = map(str, dataM.split(":")[:2])
            wait40.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'input[placeholder="Email, điện thoại hoặc Skype"]',
                    )
                )
            ).send_keys(username)
            wait40.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'input[type="submit"]')
                )
            ).click()
            # wait40.until(
            #     EC.element_to_be_clickable(
            #         (By.CSS_SELECTOR, '#otherIdpLogin')
            #     )
            # ).click()
            wait40.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//input[@aria-labelledby="passwordTitle"]')
                )
            ).click()
            wait40.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//input[@aria-labelledby="passwordTitle"]')
                )
            ).send_keys(password)
            wait40.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '*[type="submit"]'))
            ).click()
            print(f"[{index}]OK")
            sleep(2)
            if "Tài khoản của bạn đã bị khóa" in str(driver.page_source):
                print(f"[{index}]{FR}Tài khoản của bạn đã bị khóa{FW}")
                driver.quit()
                RUNNINGCHROME[index] = False
                return
            if (
                "Bạn đã cố gắng đăng nhập quá nhiều lần bằng mật khẩu hoặc tài khoản không chính xác."
                in str(driver.page_source)
            ):
                print(
                    f"[{index}]{FR}Bạn đã cố gắng đăng nhập quá nhiều lần bằng mật khẩu hoặc tài khoản không chính xác.{FW}"
                )
                driver.quit()
                RUNNINGCHROME[index] = False
                return
            if "Bỏ qua bây giờ" in str(driver.page_source):
                print(f"[{index}]Bỏ qua bây giờ (7 ngày đến khi bắt buộc)")
                # wait40.until(EC.visibility_of_element_located((By.XPATH,  "//a[contains(text(),'Bỏ qua bây giờ')]"))).click()
                MAILTMRESULT = MAILTM.get_account()
                wait40.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "input[placeholder='ai_do@example.com']")
                    )
                ).send_keys(MAILTMRESULT.address)
                wait40.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'input[type="submit"]')
                    )
                ).click()
                wait40.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "input[placeholder='Mã']")
                    )
                )
                code = ""
                for i in range(2):
                    for i in range(5):
                        message = MAILTMRESULT.get_messages(page=1)
                        print(f"[{index}]Đang lấy mã")
                        if len(message) > 0:
                            if "Mã bảo mật" in str(message[0].text):
                                mess = str(message[0].text).split("Mã bảo mật")[1]
                            print(f"[{index}]{message[0].text}")
                            code = re.findall(r"\d+", mess)[0]
                            break
                        sleep(5)
                    print(f"[{index}]{FG}CODE: {code}{FW}")
                    wait40.until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, "input[placeholder='Mã']")
                        )
                    ).send_keys(str(code))
                    wait40.until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, '*[type="submit"]')
                        )
                    ).click()
                    break
                open("VERYMAIL.txt", encoding="utf-8", mode="a+").write(
                    f"{username}|{password}|{MAILTMRESULT.address}|{MAILTMRESULT.password}\n"
                )
                sleep(10)
            if "Duy trì đăng nhập?" in str(driver.page_source):
                print(f"[{index}]DUY TRÌ ĐĂNG NHẬP")
                open("Response/ok.txt", encoding="utf-8", mode="a+").write(
                    f"{username}:{password}\n"
                )
                wait40.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, '*[type="submit"]')
                    )
                ).click()
                driver.refresh()

                sleep(3)
                if "Không còn cần đến mật khẩu" in str(driver.page_source):
                    print(f"[{index}]Không còn cần đến mật khẩu")
                    wait40.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '//a[@id="iCancel"]')
                        )
                    ).click()
                    sleep(3)
                # DONE LOGIN
                fillInfo(driver=driver) 
                # DONE FILL AND CAPTCHA 
                print(f"[{index}]Switch Default")
                
                while True:
                    driver.switch_to.default_content()
                    if "Something went wrong" in str(driver.page_source):
                        print(f"[{index}]Something went wrong")
                        driver.quit()
                        RUNNINGCHROME[index] = False
                        return
                    
                    # driver.execute_script("scrollBy(0,-500);")
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);",
                        wait40.until(
                            EC.visibility_of_element_located(
                                (By.XPATH, '//input[@id="sse-vnext-email-input"]')
                            )
                        ),
                    )
                    EMAIL = str(mailQueue.get())
                    try:
                        driver.execute_script(
                            "arguments[0].scrollIntoView(true);",
                            wait40.until(
                                EC.visibility_of_element_located(
                                    (By.XPATH, '//input[@id="sse-vnext-email-input"]')
                                )
                            ),
                        )
                        wait40.until(
                            EC.visibility_of_element_located(
                                (By.XPATH, '//input[@id="sse-vnext-email-input"]')
                            )
                        ).clear()
                        wait40.until(
                            EC.visibility_of_element_located(
                                (By.XPATH, '//input[@id="sse-vnext-email-input"]')
                            )
                        ).send_keys(EMAIL.split(":")[0])
                    except ElementNotInteractableException:
                        RUNNINGCHROME[index] = False
                        raise Exception(f"[{index}]Không thể nhập mail")
                    wait40.until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, '*[type="submit"]')
                        )
                    )
                    sleep(3)
                    wait40.until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, '*[type="submit"]')
                        )
                    ).click()
                    print(f"[{index}]Submit")
                    # ===================
                    NotAccess = False
                    for i in range(2):
                        sleep(10)
                        if "Something went wrong" in str(driver.page_source):
                            print(f"[{index}]{FR}Something went wrong{FW}")
                            driver.quit()
                            RUNNINGCHROME[index] = False
                            return
                        if "You do not have access" in str(driver.page_source):
                            print(f"[{index}]{FR}You do not have access{FW}")
                            refreshMail(mail=EMAIL.split(":")[0], status=1)
                            driver.refresh()
                            NotAccess = True
                            break
                        else:
                            try:
                                wait40.until(
                                    EC.visibility_of_element_located(
                                        (By.XPATH, '//input[@id="sse-vnext-fname-input"]')
                                    )
                                )
                                break
                            except:
                                driver.refresh()
                                print(f"[{index}]LOADING...")

                    # --------------
                    if NotAccess == True:
                        fillInfo(driver=driver)
                        driver.execute_script("window.scrollTo(0, 30);")
                    else:
                        # ===================
                        if (
                            "Your email domain is not currently registered with us. You can choose another verification method."
                            in str(driver.page_source)
                        ):
                            print(
                                f"[{index}][-]{EMAIL} - {FY}Your email domain is not currently registered with us. You can choose another verification method.{FW}"
                            )
                            refreshMail(mail=EMAIL.split(":")[0], status=1)
                        elif (
                            "Verification email has been sent to the school email you provided. Please follow the instructions in the email to complete offer activation."
                            in str(driver.page_source)
                        ):
                            print(
                                f"[{index}][-]{EMAIL} - {FG}Verification email has been sent to the school email you provided. Please follow the instructions in the email to complete offer activation.{FW}"
                            )
                            refreshMail(mail=EMAIL.split(":")[0], status=0)
                        else:
                            print(f"[{index}][-]{EMAIL} - Trường hợp không xác định")
                            driver.quit()
                            RUNNINGCHROME[index] = False
                            return

            elif (
                "Tài khoản hoặc mật khẩu của bạn không chính xác. Nếu bạn không nhớ mật khẩu của mình"
                in str(driver.page_source)
            ):
                print(f"[{index}]{FR}SAI PASSWORD - LƯU FILE ERRORPASSWORD.txt{FW}")
                open("Response/ERRORPASSWORD.txt", encoding="utf-8", mode="a+").write(
                    f"{username}:{password}\n"
                )
                driver.quit()
                RUNNINGCHROME[index] = False
                return
            elif "Cần thêm thông tin" in str(driver.page_source):
                print(
                    f"[{index}]{FR}Cần thêm thông tin - LƯU FILE ERRORMOREINFO.txt{FW}"
                )
                open("Response/ERRORMOREINFO.txt", encoding="utf-8", mode="a+").write(
                    f"{username}:{password}\n"
                )
                driver.quit()
                RUNNINGCHROME[index] = False
                return
            elif "Chúng tôi đã phát hiện hoạt động bất thường ở tài khoản" in str(
                driver.page_source
            ):
                print(
                    f"[{index}]{FR}Chúng tôi đã phát hiện hoạt động bất thường ở tài khoản - LƯU FILE BATTHUONG.txt{FW}"
                )
                open("Response/BATTHUONG.txt", encoding="utf-8", mode="a+").write(
                    f"{username}:{password}\n"
                )
                driver.quit()
                RUNNINGCHROME[index] = False
                return
            else:
                print(f"[{index}]{FR}Không xác định - LƯU FILE ERRORMOREINFO.txt{FW}")
                open("Response/ERRORMOREINFO.txt", encoding="utf-8", mode="a+").write(
                    f"{username}:{password}\n"
                )
                driver.quit()
                RUNNINGCHROME[index] = False
                return

        driver.quit()
    except NetworkError:
        print(f"[{index}] CAN'T CONNECT TO WEB")
        RUNNINGCHROME[index] = False
        return
    except Exception as e:
            print(f"[{index}] Lỗi: LƯU FILE ERROR.txt")
            RUNNINGCHROME[index] = False
            return


def saveData(filename, value):
    for dataM in value:
        username, password = map(str, dataM.split(":")[:2])
        open(filename, encoding="utf-8", mode="a+").write(f"{username}:{password}\n")


def do_stuff(jobs, index, keyProxy):
    while not jobs.empty():
        value = jobs.get()
        with open("account.txt", "w", encoding="utf-8") as f:
            queue_copy = deque(jobs.queue)
            for listData in queue_copy:
                for data in listData:
                    username, password = map(str, data.split(":")[:2])
                    f.write(f"{username}:{password}\n")

        main(index, value, keyProxy)
        jobs.task_done()


if __name__ == "__main__":
    mailQueue = Queue()
    listEndMail = [i.replace(".txt", "") for i in os.listdir("SUCCESS")]

    listMail = [
        i.strip()
        for i in open("EDUACCOUNT.txt", mode="r", encoding="utf-8").readlines()
        if (
            "UNKNOWN:" not in i
            and "@" in i
            and ":" in i
            and len(str(i).split(":")) == 2
        )
    ]
    for mail in listMail:
        for endMail in listEndMail:
            if endMail in mail:
                listMail.remove(mail)
                refreshMail(mail=endMail.split(":")[0], status=0)

    print(f"{FG} LỌC MAIL HOÀN TẤT: {len(listMail)} hợp lệ{FW}")
    for i in listMail:
        mailQueue.put(i.strip())

    jobs = Queue()
    keyProxy = open("keyproxy.txt", "r", encoding="utf-8").read().strip()
    print(f"{FG} KEY PROXY WW: {keyProxy}{FW}")
    # ProxyString, ipcc = getNewIp(api_key=keyProxy)
    # print(f'{FG} CHANGE IP: {ProxyString}{FW}')
    listDataAccount = open("account.txt", encoding="utf-8", mode="r").readlines()

    dataGet = []
    row = 0
    # Lặp qua listDataAccount và đưa vào hàng đợi jobs
    for dataAccount in listDataAccount:
        dataGet.append(dataAccount.strip())
        if len(dataGet) >= 1:
            jobs.put(dataGet.copy())  # Sử dụng copy để tránh tình trạng tham chiếu
            dataGet.clear()
    jobs.put(dataGet.copy())
    dataGet.clear()

    # In thông báo chuẩn bị chạy
    print("Đang Chuẩn Bị Chạy:", jobs.qsize(), "Tài Khoản!")
    MYCOUNTTHREAD = int(input("Nhập số luồng: "))
    for index in range(MYCOUNTTHREAD):
        print(f"Luồng {index}: Bắt đầu tạo chạy!")
        worker = threading.Thread(
            target=do_stuff,
            args=(
                jobs,
                index,
                keyProxy,
            ),
        )
        worker.start()
        sleep(3)
    jobs.join()
