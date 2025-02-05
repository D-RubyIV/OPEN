import random
import re
import string
import cloudscraper
import requests
from unidecode import unidecode

scraper = cloudscraper.create_scraper()


# Hàm tạo tên người Việt Nam không có dấu ngẫu nhiên
def tao_ten(ho):
    ho = ho.replace('\'', '').split()
    ho_random = ho[0]
    dem_random = ho[1]
    ten_random = ho[2]
    namerd = [ho_random[0],dem_random[0],ten_random]
    random.shuffle(namerd)
    random.shuffle(ho)
    email = (''.join(namerd)+str(random.randint(10, 10000))[:12]).lower() + '@gmail.com'
    # email = (''.join(namerd)+str(random.randint(10, 10000))[:12]).lower() + '@' + ''.join(random.choice(string.ascii_letters.lower()) for _ in range(random.randint(4,7))) + '.' + ''.join(random.choice(string.ascii_letters.lower()) for _ in range(random.randint(2,3)))
    return " ".join(ho), email

# Hàm tạo ngày tháng năm sinh ngẫu nhiên trong khoảng năm 1950 đến 2000
def tao_ngay_sinh():
    ngay = str(random.randint(1, 28)).zfill(2)
    thang = str(random.randint(1, 12)).zfill(2)
    nam = str(random.randint(1950, 1999))
    return ngay + thang + nam[2:]

# Hàm tạo username từ tên người và ngày tháng năm sinh
def tao_username(ten_nguoi, ngay_sinh):
    username = ten_nguoi.lower().replace(" ", "") + ''.join(random.sample('1234567890', len(ngay_sinh)))
    lenght = random.randint(13, 15)
    # Đảm bảo username có độ dài từ 2 đến 15 ký tự
    if len(username) > 12:
        # Nếu username dài hơn 15 ký tự, bỏ phần "dem" đi
        dem_random = ten_nguoi.split()[1]
        username = ten_nguoi.lower().replace(" ", "").replace(dem_random.lower(), "") + ''.join(random.sample('1234567890', len(ngay_sinh)))
    if len(username) > lenght:
        username = username[:lenght-1] + ''.join(random.sample('1234567890', len(ngay_sinh)))
    return username[:lenght]

def generate_random_password():
    # Xác định độ dài ngẫu nhiên từ 8 đến 12
    password_length = random.randint(8, 12)
    
    # Danh sách các chữ cái và số
    letters_and_digits = string.ascii_letters + string.digits
    
    # Chọn một chữ cái ngẫu nhiên cho mật khẩu
    password = random.choice(string.digits)
    
    # Chọn các ký tự ngẫu nhiên cho mật khẩu, bao gồm số
    password += ''.join(random.choice(letters_and_digits) for _ in range(password_length - 1))
    
    # Trộn các ký tự để tạo mật khẩu cuối cùng
    password = ''.join(random.sample(password, len(password)))
    
    return password

# Số lượng username cần tạo
# so_luong_usernames = 30
so_luong_usernames = int(input("Nhập số lượng tài khoản muốn tạo (VD: 5000): "))
print("--->Để trống nếu bạn muốn tạo tên ngẫu nhiên!")
my_name = input("Nhập tên của bạn (VD: LY TIEU LONG): ")
dtjson = {  'action': 'ten_tieng_viet_random',
            'gender': 'male',
            'is_fullname': 'yes',
            'surname_option': 'random',
            'so_luong': so_luong_usernames,
            'lang': 'vi}'}
bank = input("1. VPBANK\n2. MB\nChọn Bank: ")
if bank == '1':
    bank = 'VPBank'
else:
    bank = "MB"

response = scraper.post('https://dichthuatphuongdong.com/tienich/do.php', data=dtjson)
names = unidecode(response.text).split('|',1)[0].split(' ,')

response1 = scraper.get('https://raw.githubusercontent.com/madnh/hanhchinhvn/master/dist/tinh_tp.json').json().values()
response2 = scraper.get('https://raw.githubusercontent.com/madnh/hanhchinhvn/master/dist/quan_huyen.json').json().values()
response3 = scraper.get('https://raw.githubusercontent.com/madnh/hanhchinhvn/master/dist/xa_phuong.json').json().values()
cities = []
for i in response1:
    cities.append(i['name_with_type'])
# for i in response2:
#     cities.append(i['name_with_type'])
# for i in response3:
#     cities.append(i['name_with_type'])
for name in names:
    nameRandom = random.choice(names).split(" ")[1]
    name += f" {nameRandom}"
    ten_nguoi, email = tao_ten(name)
    
    ngay_sinh = tao_ngay_sinh()
    username = tao_username(ten_nguoi, ngay_sinh)
    ten_nguoi = ten_nguoi.upper()
    # bank = random.choice(['VPBANK'])
    city = random.choice(cities).lower().replace('\'','')
    letters = re.findall(r'[a-zA-Z]', username)
    password = ''.join(letters) + str(random.randint(10000, 99999))
    password = password[:8] + str(random.randint(1, 1000))
    password = ''.join(random.sample(password, len(password)))
    # pass_rut1 = password[:-2]
    # pass_rut2 = ''.join(random.choice(string.digits) for _ in range(random.randint(6,10)))
    pass_rut = ''.join(random.choice(string.digits) for _ in range(random.randint(6,6)))
    # pass_rut = random.choice([pass_rut1, pass_rut2])
    password = random.choice([generate_random_password(), password])
    phone1 = random.choice(['9','3'])+''.join(random.choice(string.digits) for _ in range(8))
    phone2 = random.choice(['52','56','58','59','69','70','76','77','78','79','70','81','82','83','87','88']) + ''.join(random.choice(string.digits) for _ in range(7))
    # phone3 = random.choice(['69']) + ''.join(random.choice(string.digits) for _ in range(6))
    # phone4 = random.choice(['21','22','23','24','25','27','28','29']) + ''.join(random.choice(string.digits) for _ in range(8))
    # phone5 = random.choice(['19']) + ''.join(random.choice(string.digits) for _ in range(5))
    phone = random.choice([phone1,phone2])
    stk = random.choice(['1','2','3','4','5','6','7','8','9']) + ''.join(random.choice(string.digits) for _ in range(random.randint(9,16)))
    if my_name == "":
            with open('username.txt', 'a', encoding='utf-8') as f:
                f.write(f'{username}|{password}|{ten_nguoi}|{ngay_sinh}|{city}|{stk}|{bank}|{pass_rut}\n')
    else:
        ten_nguoi = my_name.upper()
        with open('username.txt', 'a', encoding='utf-8') as f:
            f.write(f'{username}|{password}|{ten_nguoi}|{ngay_sinh}|{city}|{stk}|{bank}|{pass_rut}\n')
print(f"Đã tạo thành công {so_luong_usernames} tài khoản!")