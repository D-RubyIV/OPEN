from queue import Queue
import threading
import base64
import re
import requests
import random
import asyncio
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
from Moudule.CaptchaWheel import CaptChaWheel

passBank = 192002
numberBank = "0102688500001"
pasAccount = "mvOCLsfq89"

chrome_options = webdriver.ChromeOptions()
    
chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{65188}")

driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options)
driver.set_page_load_timeout(30)
driver.set_page_load_timeout(30)
driver.set_window_size(600,1000)
action = ActionChains(driver)
wait = WebDriverWait(driver, 40)
wait20 = WebDriverWait(driver, 40)
wait10 = WebDriverWait(driver, 40)
wait05 = WebDriverWait(driver, 5)
wait02 = WebDriverWait(driver, 2)

username = "dion1000111"
password = "sdui989"
fullName = "PHAM HOAI ANH"
phone = "833486759"

driver.get("https://www.nbvn777.com/m/home?fbclid=IwAR09hYp01buVJbxEvA7WvbSg9JiflV8nb31dNtljyI6A-gxS08GOoHr6v4k_aem_AfdFai2SuV2eXNq2x9tFF_YqkWWc_a1bYR-8IykBEAVQS4rb65mLb_B0cZzcGAXBwFlz3pZfoNyB4g8-vl-6DeJV")

if '<div class="popup_title">vip</div>' in str(driver.page_source):
    wait10.until(EC.presence_of_element_located((By.XPATH, "//div[@class='am-navbar-title close-btn']"))).click()

wait10.until(EC.presence_of_element_located((By.XPATH, "//span[@class='btn-register']"))).click()
wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Nhập tên đăng nhập *']"))).send_keys(username)
wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Mật khẩu *']"))).send_keys(password)
wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Xác nhận lại mật khẩu *']"))).send_keys(password)
wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Số điện thoại ']"))).send_keys(phone)

while "Mã xác nhận *" in str(driver.page_source):
    eleCaptcha = wait10.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='captcha']")))
    codeCaptCha = str(CaptChaWheel.sloveGPU(base64_img=eleCaptcha.get_attribute("src"), pathImg=f"Images/{1}_img.png")).replace("-","")
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
wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='TÌM SỐ']"))).send_keys("99")
wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='query-submit ']"))).click()
countMoney = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='money-box']"))).find_element(By.XPATH,"div[1]").text
for i in range(int(float(countMoney))-1):
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='sc-plus']"))).click()
wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='submit-btn btn']"))).click()
sleep(3)
wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'submit-btn') and contains(@class, 'btn') and text()='Xác nhận']"))).click()

