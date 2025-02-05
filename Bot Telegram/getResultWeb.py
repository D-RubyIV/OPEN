import hashlib
import random
import string
import time
import requests
import json

class Game82VN():



    def __init__(self):
        self.base = "https://82vn82vnapi.com/"
        self.headers = {
        "authority": "82vn82vnapi.com",
        "method": "POST",
        "path": "/api/webapi/GetTRXNoaverageEmerdList",
        "scheme": "https",
        # "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "30",
        "content-type": "application/json; charset=utf-8",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzEwNDg3ODYxIiwibmJmIjoiMTcxMDQ4Nzg2MSIsImV4cCI6IjE3MTA0ODk2NjEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIzLzE1LzIwMjQgMzowMTowMSBQTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6IjYzMTk0MyIsIlVzZXJOYW1lIjoiODQ4MzM0ODY5MzIiLCJVc2VyUGhvdG8iOiIxIiwiTmlja05hbWUiOiJNZW1iZXJOTkdZRThQWSIsIkFtb3VudCI6IjAuMDAiLCJJbnRlZ3JhbCI6IjAiLCJMb2dpbk1hcmsiOiJINSIsIkxvZ2luVGltZSI6IjMvMTUvMjAyNCAyOjMxOjAxIFBNIiwiTG9naW5JUEFkZHJlc3MiOiIxLjU1LjY5LjcwIiwiRGJOdW1iZXIiOiIwIiwiSXN2YWxpZGF0b3IiOiIwIiwiS2V5Q29kZSI6IjEiLCJUb2tlblR5cGUiOiJBY2Nlc3NfVG9rZW4iLCJQaG9uZVR5cGUiOiIwIiwiVXNlclR5cGUiOiIwIiwiVXNlck5hbWUyIjoiIiwiaXNzIjoiand0SXNzdWVyIiwiYXVkIjoibG90dGVyeVRpY2tldCJ9.Oe6zOmPK4yogq8LGs_icTaZqfAd2iYC6fQQDo83P-UM",
        "origin": "https://82vn.com",
        "referer": "https://82vn.com/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48"
        }
    
    def random_hash(self):
        characters = string.ascii_letters + string.digits
        input_string = ''.join(random.choice(characters) for _ in range(16))  # Tạo một chuỗi ngẫu nhiên có độ dài 16 ký tự
        md5_hash = hashlib.md5(input_string.encode()).hexdigest()
        return md5_hash

    def getResult(self):
        randdomCode = self.random_hash()
        timeStp = int(time.time())
        data_to_sign =  str(timeStp) + randdomCode
        url = f"https://82vn82vnapi.com/api/webapi/GetTRXNoaverageEmerdList"
        data = {
            "pageSize": 10,
            "pageNo": 1,
            "typeId": 13,
            "language": 2,
            "random": "4c33f611fda04770a091e77bfa33d0a0",
            "signature": "1BCE8E97D889D4F65E7E6128CAF89859",
            "timestamp": 1710488942
        }
        print(data)
        result = requests.post(url=url, headers=self.headers, data=json.dumps(data))
        print(result.text)
        allResult = result.json()["data"]["gameslist"]

        listLN = ""
        for result in allResult:
            listLN += "L" if int(result["Number"]) >= 5 else "N"
        
        kiSoUpdate = allResult[0]["IssueNumber"]
        blockNumber = allResult[0]["BlockNumber"]
        print([listLN, kiSoUpdate, blockNumber])
        return listLN, kiSoUpdate, blockNumber


