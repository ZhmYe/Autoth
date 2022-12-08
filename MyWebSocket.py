import websocket
import base64
class websocketInstance:
    def __init__(self, url) -> None:
        self.message_number = 0
        self.initStr = [
            base64.b16decode('7b2241757468546f6b656e223a22227d'.upper()),
            base64.b16decode('317b22636f6c756d6e73223a3133382c22726f7773223a36317d'.upper())
        ]
        self.headers = {
            'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
            'Sec-WebSocket-Key': 'oYuZHR5Mj/VB9irNeNyMeA==',
            'Sec-WebSocket-Protocol': 'tty',
            'Sec-WebSocket-Version': '13',
            'Upgrade': 'websocket'
        }
        self.ws = websocket.WebSocketApp('ws://{}.proxy.nscc-gz.cn:8888/ws'.format(url), header=self.headers, on_open = self.on_open, on_message= self.on_message, on_error=self.on_error)
    def on_error(self, ws, error):
        print(error)
        ws.close()
    def on_open(self, ws):
        # print('     Websocket: open')
        for char in self.initStr:
            # print(char)
            ws.send(char)
    def on_message(self, ws, message):
        self.message_number += 1
        # print(message)
        # print(self.message_number)
        if self.message_number >= 31:
            self.ws.close()
            # print("     WebSocket: close")
    def run(self):
        self.ws.run_forever()
