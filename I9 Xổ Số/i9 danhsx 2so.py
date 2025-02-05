import cloudscraper
from time import sleep
import fake_useragent
from queue import Queue 
import threading
import re
import random
import requests
import string
import hashlib, zipfile, os

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from CaptchaWheel import CaptChaWheel

jobs = Queue()
ua = fake_useragent.UserAgent(min_percentage=0.9)

def random_hash():
    characters = string.ascii_letters + string.digits
    input_string = ''.join(random.choice(characters) for _ in range(16))  # Tạo một chuỗi ngẫu nhiên có độ dài 16 ký tự
    md5_hash = hashlib.md5(input_string.encode()).hexdigest()
    return md5_hash
def new_ip(api_key):
    headers = {
    "Accept":"application/json",
    "Content-Type":"application/json",
    }
    ip_me = requests.get('https://api.ipify.org/?format=json', headers=headers).json()["ip"]
    if ':'in api_key:
        ipp, port, user, pas_ = api_key.split(":")
        ip = f"http://{user}:{pas_}@{ipp}:{port}"
        proxies = {"http": ip , "https": ip}
        return ip, proxies
    elif str(api_key).count("-") == 5:
        while True:
            listProvine = [i["id"] for i in requests.get("https://wwproxy.com/api/client/province?search_text=").json()["data"]]
            ip = requests.get(f"https://wwproxy.com/api/client/proxy/available?key={api_key}&provinceId={random.choice(listProvine)}").json()
            print(ip)
            if ip["errorCode"] == 0:
                ipcc = ip['data']['proxy']
                proxies = {"http": ipcc , "https": ipcc}
                return ipcc, proxies
            elif ip["errorCode"] == 1:
                for ll in range(5, -1, -1):
                    print(f"Vui lòng đợi {str(ll)} để đổi ip lần nữa        ", end="\r")
                    sleep(1)
    elif '-' in api_key:
        while True:
            try:
                ip = requests.get(f"https://app.proxydt.com/api/public/proxy/get-new-proxy?license={api_key}&authen_ips={ip_me}", headers=headers).json()
            except Exception as e:
                continue
            
            if ip["code"] == 1:
                ipcc = ip['data']['http_ipv4']
                proxies = {"http": ipcc , "https": ipcc}
                return ipcc, proxies
            elif ip["code"] == 0:
                if "Không tìm thấy license" in str(ip) or "Yêu cầu license key & whitelist Ip!" in str(ip) or 'Token không hợp lệ.' in str(ip):
                    print(ip)
                    return "KEYEXPIRED"
                for ll in range(5, -1, -1):
                    print(f"Vui lòng đợi {str(ll)} để đổi ip lần nữa        ", end="\r")
                    sleep(1)
    else:
        while True:
            try:
                ip = requests.get(f"http://proxy.tinsoftsv.com/api/changeProxy.php?key={api_key}&location=0", headers=headers).json()
            except Exception as e:
                continue
            if ip['success']:
                ipcc = ip['proxy']
                ipcc = 'http://' + ipcc
                if 'None:' in ipcc:
                    continue
                proxies = {"http": ipcc , "https": ipcc}
                return ipcc, proxies
            else:
                try:
                    timee = int(re.findall(r'\d+', ip['description'])[0]) # type: ignore
                    for ll in range(timee, -1, -1):
                        print(f"Vui lòng đợi {str(ll)} để đổi ip lần nữa        ", end="\r")
                        sleep(1)
                except:
                    print(ip['description'])
                    print('Có key tinsoft lỗi!')
def solve(base64_img):
    if 'data:image/png;base64,' not in base64_img:
        base64_img = f'data:image/png;base64,{base64_img}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'XSRF-TOKEN=eyJpdiI6IkpVTlIzS25jRWpkUklyZ1RnODdDRGc9PSIsInZhbHVlIjoieWdmTUhvQnlldlJwR1FFOHRXb2Q3N3EydzlWdElXdmFrVTJiNFhSaEJ3VFIrTjd3Z1IyN3Q3dFZmd2JIWE54UDFadkVrWElhZEkzTnFpNGx1MGxqSkRWRWRoc1QzODQ1aXIrc2NjMWdSZms0cFJDTWxnOStZaEE5RHMvL01Wc2siLCJtYWMiOiJhNDM2MjI2YmM2MjhjNDdhZWVkY2YzODM5NGQyZjQ1YmIyN2I1MTg0NmIyOWJkOGJjNTgxYTZiNGFjZWM5OWMyIiwidGFnIjoiIn0%3D; image_to_text_session=eyJpdiI6IkNHS2dWODRsSkFZSVVGTkJBSm11YlE9PSIsInZhbHVlIjoiUUZONjhkL0taWG9nWTdhUWdYaEpTbWVWSy9hNXZ2RnV2NlFBNHBFdnViVDN1cWZjYVBKZm9MVzRLQkJhMmZMeU4wMzhmVWpqbmgyUktCNHZsSWk2TEpFcTFhTlJMQWlQUC8yOXlzYTZ4a2VJVXgvRDVqa2xveDh2c2tNa29lM3EiLCJtYWMiOiIxMmZlM2U5NGQ4OWZiOGZmOTZiOGZjYjI5ODgxNGI2OWE4YWRhYTIxZTFjNDc5OGY3Yjg5N2I2ZDMyYThjZWI5IiwidGFnIjoiIn0%3D; _ga_KJ1ZFKYBEY=GS1.1.1695650159.3.0.1695650159.0.0.0; _gid=GA1.2.1122328108.1695650160; _gat_gtag_UA_200597024_7=1; _ga_3YL3KYQTJM=GS1.1.1695650160.3.0.1695650160.0.0.0; _ga=GA1.1.24943833.1691925264; _clck=1971chf|2|ffb|0|1320; _clsk=1pq052n|1695650161376|1|1|u.clarity.ms/collect; twk_idm_key=feeMWv1mT4N1gDW-VuvMU; TawkConnectionTime=0; twk_uuid_63e5e15cc2f1ac1e203275f4=%7B%22uuid%22%3A%221.2BiUXGoOb2JiAjcpujbN9MziFKAVgkJyPZz9TecPGdDI8Gd4j0f0VVmcWu7VgLT9eOz73gZTi6JKrvkAoVhxfCOS2lSKFLYJSjkcnaBK8obb8SpRSyq08HEebRm%22%2C%22version%22%3A3%2C%22domain%22%3A%22imagetotext.info%22%2C%22ts%22%3A1695650163632%7D',
    }
    response = requests.get('https://www.imagetotext.info/', headers=headers)
    token = response.text.split('content="', 3)[-1].split('" />',1)[0]
    payload = {
        'base64': f'{base64_img}',
        'imgname': 'ho.png',
        'count': '0',
        '_token': token,
    }
    response = requests.post('https://www.imagetotext.info/image-to-text', headers=headers, data=payload)
    texxt = response.json()
    result = texxt['text'][-4:]
    return result
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"117.0.0"
}
"""

def background_js(PROXY_HOST,PROXY_PORT,PROXY_USER,PROXY_PASS):
    return """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None, api_key=''):
    if '|' in api_key:
        new_ip(api_key)
        ipp, port, user, pas_ = api_key.split(":",3)
        pas_, linkchange = pas_.split('|')
    elif ':'in api_key:
        ipp, port, user, pas_ = api_key.split(":",3)
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js(ipp,port,user,pas_))
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--user-agent=%s' % user_agent)
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    return driver
def run(location, data, key):
    global sode
    useragent = ua.chrome
    headers = {
        'User-Agent':useragent
    }
    fingerprint = random_hash()
    try:
        username, password, ten, ngay_sinh, city, stk, bank, passrut = map(str, data.split('|'))
    except:
        username, password = map(str, data.split('|'))
    print(username, password)
    ipcc, proxies = new_ip(key)
    scraper = cloudscraper.create_scraper()
    scraper.headers.update(headers)
    scraper.proxies.update(proxies) # type: ignore
    while True:
        captcha = scraper.post('https://www.i9bet151.com/api/0.0/Home/GetCaptchaForLogin')
        captcha = captcha.json()
        base64_img, captchauuid = captcha['image'], captcha['value']
        # captcha_solved = solve(f'{base64_img}')
        # captcha_solved = CaptChaWheel.ImgtoTextORC_V1(base64Img=f'{base64_img}', engine=1, proxies=proxies)
        captcha_solved = CaptChaWheel.sloveGPU(base64_img=f'{base64_img}', nameImg=str(key))
        payload = {"account":username,"password":password,"checkCode":captcha_solved,"checkCodeEncrypt":captchauuid,"fingerprint":fingerprint}
        login = scraper.post('https://www.i9bet151.com/api/0.0/Login/login', json=payload)
        if 'Lỗi mã xác minh' in login.text:
            continue
        elif "Mã xác minh không được để trống" in login.text:
            continue
        elif 'LoginToken' in login.text:
            token = login.json()['LoginToken']['AccessToken']
            break
        else:
            print(login.text)
            return
    scraper.headers.update({'Authorization':f'Bearer {token}'}) # type: ignore
    while True:
        tp = scraper.get('https://www.i9bet151.com/api/1.0/account/loginToGame?SupplierType=Tp&gid=1568')
        link_ = tp.json()['Result']['Url']
        # link = scraper.get(link_)
        # link = link.url
        if link_:
            break
        # print(link_)
    if ':' in key:
        driver = get_chromedriver(use_proxy=True, user_agent=ua.chrome,api_key=key)
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--proxy-server={ipcc}')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument(f"user-agent={useragent}")
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        # chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
    # driver.set_page_load_timeout(10)
    actions = ActionChains(driver)
    if location == 1:
        driver.set_window_position(500,0)
    driver.set_window_size(500,900)

    wait = WebDriverWait(driver, 20)
    wait10 = WebDriverWait(driver, 10)
    wait5 = WebDriverWait(driver, 5)
    wait1 = WebDriverWait(driver, 1)

    for i in range(5):
        try:
            driver.get(link_)
            sleep(5)
            break
        except:
            continue
    for i in range(10):
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[2]/div[3]/div/div[3]'))).click()
            break
        except:
            driver.refresh()
            sleep(10)
    sleep(5)
    if "OKBtn" in driver.page_source:
        wait5.until(EC.presence_of_element_located((By.XPATH, '//div[@class="OKBtn"]'))).click()
    sleep(3)
    cuoc = driver.find_element(By.XPATH, '//div[@id="lotteryInfo"]//div[@class="txtBlue"]').text
    if "0." in cuoc: 
        print("Ko du Tien")
        return
    cuoc = int(float(cuoc))
    sode = sode%100
    so_chon = sode
    sode +=1

    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Đuôi']"))).click()
    bangsx = wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@class="mixBetCardVietnam"]/div[{so_chon+1}]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="TicketCheckBtn active"]'))).click()
    for i in str(cuoc):
        wait.until(EC.element_to_be_clickable((By.XPATH, f'//div[contains(@class, "keyboardNBBtn")][text()="{i}"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Đặt cược']"))).click()
    for i in range(30):
        if "Đặt cược thành công" in driver.page_source:
            print(data, "đánh thành công, số: %s"%so_chon)
            with open("accdanhsx.txt", "a+", encoding="utf-8") as file:
                file.write("%s|số đề: %s, số tiền: %s\n"%(data, so_chon, cuoc))
            break
    sleep(3)
    driver.quit()
def do_stuff(jobs, location, key):
    while not jobs.empty():
        value = jobs.get()
        try:
            run(location, value, key)
        except Exception as e:
            print(e)
            pass
        with open('acc.txt', 'w', encoding='utf-8') as f:
            for username in jobs.queue:
                f.write(username+'\n')
        jobs.task_done()
try:        
    with open("accdanhsx.txt", "r", encoding='utf-8') as f:
        sode = f.readlines()[-1].split("số đề: ")[1].split(", số")[0]
        sode = int(sode)
except:
    sode = 0
with open('acc.txt', 'r', encoding='utf-8') as f:
    usernames = [i.strip() for i in f.readlines() if i != '\n']
for i in usernames:
    jobs.put(i)
with open('keys.txt', 'r', encoding='utf-8') as f:
    keys = [i.strip() for i in f.readlines() if i != '\n']

if __name__ == "__main__":
    print("Chuẩn bị chạy", jobs.qsize(), "tài khoản!")
    for location in range(len(keys)):
        sleep(location)
        print(f'Luồng {location}: Bắt đầu chạy!')
        key = keys[location]
        worker = threading.Thread(target=do_stuff, args=(jobs,location,key,))
        worker.start()

    jobs.join()
    print('Tất cả đã hoàn thành!')