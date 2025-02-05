
import base64
import io
import json
import time
import requests
from PIL import Image, ImageOps, ImageFilter
from io import BytesIO
import easyocr

class CaptChaWheel():
    def __init__(self) -> None:
        pass
    
    def sloveGPU(base64_img, pathImg):
        if 'data:image/png;base64,' not in base64_img:
            base64_img = f'data:image/png;base64,{base64_img}'

        image_data = base64.b64decode(str(base64_img).replace("data:image/png;base64,",""))
        image = Image.open(BytesIO(image_data))
        image = image.convert('L')  # Chuyển đổi sang ảnh đen trắng
        # image = ImageOps.expand(image, border=30, fill='black')
        image.save(pathImg)
        reader = easyocr.Reader(['en'], gpu=True) # this needs to run only once to load the model into memory
        result = reader.readtext(pathImg)
        for (bblox, text, prob) in result:
            return text
        
    def solveImgToText(self, base64_img, proxies):
        if 'data:image/png;base64,' not in base64_img:
            base64_img = f'data:image/png;base64,{base64_img}'

        image_data = base64.b64decode(str(base64_img).replace("data:image/png;base64,",""))
        image = Image.open(BytesIO(image_data))
        image = image.convert('L')  # Chuyển đổi sang ảnh đen trắng
        image = ImageOps.expand(image, border=30, fill='black')
        image.save("image.jpg")
        output_buffer = BytesIO()
        image.save(output_buffer, format="JPEG")  # Chọn định dạng phù hợp với server nhận diện
        while True:
            files = {
                "imgArr": ("image.jpg", open("image.jpg", "rb")),
                "count": (None, "0")  # Assuming you want to send "0" as a string
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                "X-Csrf-Token": 'QNELhkc7VF5BDvqi7pFE4anm3bHcl58z20EXO3il',
                "Cookie": "_sharedID=cc73bd7c-7c97-452d-86e6-f2709f1f1fc6; _sharedID_cst=TyylLI8srA%3D%3D; _lr_env_src_ats=false; cto_bundle=yfXf519JeG5ZN2U4OEZsZkkxTSUyRkdCYWVsZEFmJTJGMGJBJTJCYUgxNEVWRzM4eVNYWnluUHRTN0VEeVUwQ3h2Nks1enF0a0REeG4zRXh3d2NRTnNaNlk0aW52QVM1MVJTVmZkczRTZk9KRWwlMkJUd0NsJTJCSkNSc2RuWTVXTSUyRjZlUGNWRXlwJTJCdVVsaVp3cFAlMkI4JTJGTmNDOHdKVFFnazlYTnclM0QlM0Q; _sharedID_last=Thu%2C%2025%20Jan%202024%2017%3A22%3A41%20GMT; _lr_retry_request=true; __gads=ID=d85f00b6f10eeaf3:T=1706108574:RT=1706204296:S=ALNI_MbObgLR8ZsRHyIVDteH6WIg7E8rbw; __gpi=UID=00000cef6c0c4175:T=1706108574:RT=1706204296:S=ALNI_MYq9tOFvmgB21ayaqNegHKJoXU6nw; XSRF-TOKEN=eyJpdiI6IndQcGlobU00K0ZwQzgvYm5EYWVPOEE9PSIsInZhbHVlIjoiRFN1Mi9QOXdPUHhtK0hMRmhnVy9ScFAzc1RNc2ZhUEpYL3BjeWtucW5JMDBlRmdKWVJjOVhQQTBBaU1DVWN0WEwxTVZwQzZvY2JTUmhraUJxbnk2cEovdEkwU2tDdUlCM0o0YUVVR3N4TXlHMk4vbHdHMklMUXRpa1g1NWYrYnIiLCJtYWMiOiJhNGJlNjBlODhkYWU2ODJjOTc5N2QzYWNiY2E3NDk5YzAyNzMyYTcxZjEzNTNiZGFhYTUzYzRkOGVlZDMyOGNmIiwidGFnIjoiIn0%3D; laravel_9_session=eyJpdiI6ImZnelRtREcyQWtyTG0xMUNXaVpxamc9PSIsInZhbHVlIjoiUmx1VjdydWc2TktJeUhrc3ZQTkVQdTV3N0VDV1ZxNWlLcWdNR3J6TVBNcHRLd0xLeVRrbUI3NnhGWk0yQkMySytZdFhmNWt0dlV4ZU9jNUoxTnJKTUhJNmYxZnFJekl4czhDb2M5QzYweHJ5R2FGUDNHeHlXenBCdnRHelRFN3oiLCJtYWMiOiI1M2ZlMGRmNTdmNjdjZWIwZTU1YzY3NWI4NjgxY2Y2Y2Q0MzQ2YzdlNzJiMDdkOWEwNzY1ZDQwNzhkNzQwZTA3IiwidGFnIjoiIn0%3D "
            }
            response = requests.post("https://www.imagetotext.io/image-to-text", headers=headers, files=files, proxies=proxies)          
            print(response.text)
            if "Just" not in str(response.text):
                texxt = response.json()
                result = texxt['text'][-4:]
                return result
            time.sleep(5)
    def ImgToText_V3(base64Image, key):
        image_data = base64.b64decode(str(base64Image).replace("data:image/png;base64,",""))
        image = Image.open(BytesIO(image_data))
        image = image.convert('L')  # Chuyển đổi sang ảnh đen trắng
        output_buffer = BytesIO()
        image.save(output_buffer, format="JPEG")  # Chọn định dạng phù hợp với server nhận diện
        # # Chuyển dữ liệu nhị phân thành base64 để gửi lên server
        processed_base64_data = "data:image/png;base64," + base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        
        url = "http://api.achicaptcha.com/createTask"
        data = {
            "clientKey": str(key),
            "task": {
                "type": "ImageToTextTask",
                "image": processed_base64_data,
                "subType": "gmx"
            }
        }
        call = requests.post(url, data=json.dumps(data))
        print(call.json())
        taskId = call.json()["taskId"]
        
        url = "http://api.achicaptcha.com/getTaskResult"
        data = {
            "clientKey": key,
            "taskId": taskId
        }
        for i in range(15):
            {'status': 'processing', 'errorId': 1, 'errorDescription': 'processing', 'solution': None}
            getResult = requests.post(url, data=json.dumps(data))
            getResult = getResult.json()
            print(getResult)
            if getResult["errorId"] == 0 and getResult["status"] == "ready":
                return getResult["solution"]
            time.sleep(3)
        return ""      
    def ImgtoTextORC_V1(base64Img, proxies , engine: int = 1, ):
        image_data = base64.b64decode(str(base64Img).replace("data:image/png;base64,",""))
        image = Image.open(BytesIO(image_data))
        image = image.convert('L')  # Chuyển đổi sang ảnh đen trắng
        image.save("image.jpg")
        output_buffer = BytesIO()
        image.save(output_buffer, format="JPEG")  # Chọn định dạng phù hợp với server nhận diện
        # # Chuyển dữ liệu nhị phân thành base64 để gửi lên server
        processed_base64_data = "data:image/png;base64," + base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        url = "https://api8.ocr.space/parse/image"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Apikey": "K89411999788957",
            "Origin": "https://ocr.space",
            "Referer": "https://ocr.space/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        }
        data = {
            "url": "",  # Set the image URL if you want to provide an image URL
            "language": "eng",
            "isOverlayRequired": True,
            "FileType": ".Auto",
            "base64Image": processed_base64_data,
            "IsCreateSearchablePDF": False,
            "isSearchablePdfHideTextLayer": True,
            "detectOrientation": False,
            "isTable": False,
            "scale": True,
            "OCREngine": engine,  # Change OCREngine value if needed
            "detectCheckbox": False,
            "checkboxTemplate": 0,
        }
        response = requests.post(url, headers=headers, data=data, proxies=proxies)
        print(response.json())
        if "TextOverlay" in str(response.text):
            if len(response.json()["ParsedResults"][0]["TextOverlay"]["Lines"]) > 0:
                result = response.json()["ParsedResults"][0]["TextOverlay"]["Lines"][0][
                    "LineText"
                ]
                print(f'RESULT: {result}')
                return result
        return ""
    