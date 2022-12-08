# import requests
import json
class shell_request:
    def __init__(self, token) -> None:
        self.token = token
    def get_headers(self):
        self.headers = {
        'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
        'Sec-WebSocket-Key': 'oYuZHR5Mj/VB9irNeNyMeA==',
        'Sec-WebSocket-Protocol': 'tty',
        'Sec-WebSocket-Version': '13',
        'Upgrade': 'websocket'
        }
        return self.headers