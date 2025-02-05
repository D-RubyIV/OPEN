import requests,json
def createTask(client_key,base_captcha):


    url = "https://api.capsolver.com/createTask"

    payload = json.dumps({
    "clientKey": client_key,
    "task": {
        "type": "ImageToTextTask",
        "websiteURL": "https://api.azhkthg1.net/",
        "module": "common",
        "body": base_captcha
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()
def getTaskResult(clientKey,resultID):
    url = "https://api.2captcha.com/getTaskResult"

    payload = json.dumps({
    "clientKey": clientKey,
    "taskId": resultID
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()