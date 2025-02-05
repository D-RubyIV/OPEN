import websocket
import json


class SOCKETAPP():
    def __init__(self) -> None:
        self.stop_receiving = False

    def on_message(self, ws, message):
        if self.is_stop_message(message):
            json_message = json.loads(message)
            #print(json_message)
            self.stop_receiving = True
            ws.close()
    
            data = json_message[1]
            gold = data['As']['gold']
            chip = data['As']['safe']
            vip = "false" if data['As']['vip'] == 0 else "true"
            dn = data['dn']
            self.callback(str(gold), str(chip), vip, dn)

    def is_stop_message(self,message):
        return '"cmd":100' in message

    def on_error(ws, error):
        pass
        #print("Error:", error)


    def on_close(self,ws,*arg):
        print("WebSocket closed")
        pass

    def on_open(self,ws, username, password, ipAdresse, userID, timeStamp, SignNature):
        # print("WebSocket opened")

        message_to_send = f'''
        [
            1,
            "Simms",
            "SC_{username}",
            "{password}",
            {{
                "info": "{{\\"ipAddress\\":\\"{ipAdresse}\\",\\"userId\\":\\"{userID}\\",\\"username\\":\\"SC_{username}\\",\\"timestamp\\":{timeStamp}}}",
                "signature": {SignNature},
                "pid": 4,
                "subi": true
            }}
        ]
        '''

        ws.send(message_to_send)

    def connect_and_listen(self,username, password, ipAdresse, userID, timeStamp, SignNature, callback_func):
        ws = websocket.WebSocketApp("wss://websocket.azhkthg1.net/websocket2",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)

        ws.on_open = lambda ws: self.on_open(ws, username, password, ipAdresse, userID, timeStamp, SignNature)
        self.callback = callback_func

        ws.run_forever()

# def handle_callback(gold, chip, vip, dn):
#     # Do whatever you want with the received values here
#     print("Received gold:", gold)
#     print("Received chip:", chip)
#     print("Received vip:", vip)
#     print("Received dn:", dn)

# connect_and_listen("fongdepchai", "phongdepchai2k8", "14.191.136.90", "887b85ea-b058-4c48-bf95-3f24a179f168", 1708692802668, "64085137064EF8104E152BC37619540FA51CE543F807DDD7995A19B2B98940EC891DFC2D6F88BEF2229440D211AB50C3F52DC00207DFB765E9E877F33FA8A8ABDF61AA9BEBAC2905F02B6C7FB673871B23CDC68D9B6F96ECD2541D24A5320B64E001E06E6988D4F3F0B7E6E05EC1D8CF2700C1CFBE9063AC9F3EE3F896109961", handle_callback)