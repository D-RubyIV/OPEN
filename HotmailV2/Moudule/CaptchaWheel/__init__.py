
import requests

class CaptChaWheel():
    def __init__(self) -> None:
        pass
    def solveImgToText(self, base64_img):
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
        