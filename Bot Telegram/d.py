from selenium import webdriver
from selenium_requests import Proxy

# Cấu hình proxy
proxy = Proxy({
    'http': 'http://127.0.0.1:8080',
    'https': 'https://127.0.0.1:8080',
})

# Tạo trình duyệt web
driver = webdriver.Chrome(proxy=proxy)

# Truy cập trang web
driver.get('https://www.google.com/')

# Ghi lại tất cả các yêu cầu HTTP
requests = proxy.get_requests()

# In ra thông tin các yêu cầu
for request in requests:
    print(request.url)