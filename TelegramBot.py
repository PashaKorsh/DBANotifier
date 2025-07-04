import requests, json
from datetime import datetime

class TelegramBot:
    def __init__(self, config):
        self.config = config

    def get(self, method, *args, **kwargs):
        return requests.get(f'https://api.telegram.org/bot{self.config.api_token}/{method}', *args, **kwargs)
    
    def post(self, method, *args, **kwargs):
        return requests.post(f'https://api.telegram.org/bot{self.config.api_token}/{method}', *args, **kwargs)
    
    def getUpdates(self):
        offset = 0
        while True:
            response = json.loads(self.get('getUpdates', params={
                'offset': offset,
                'timeout': 5,
                'allowed_updates': '["message"]'
            }).text)
            for update in response['result']:
                offset = update['update_id'] + 1
                if 'message' in update and datetime.fromtimestamp(update['message']['date'] + 30) >= datetime.now():
                    yield update
    
    def sendMessage(self, text, chat_id):
        return self.post('sendMessage', data={'text': text, 'chat_id': chat_id})