import requests
import json

def get_balance(service, client_key):
    url = "https://api.capsolver.com/getBalance" if service == "Capsolver" else "https://api.2captcha.com/getBalance"
    payload = json.dumps({"clientKey": client_key})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)
    return response
