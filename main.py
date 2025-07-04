import time, threading
from datetime import datetime, timedelta
from pydantic_settings import BaseSettings, SettingsConfigDict
from TelegramBot import TelegramBot
from TableParser import TableParser

class Settings(BaseSettings):
    api_token: str
    table_path: str
    reasons_location: str
    reasons_count: int
    dba_count: int
    reboot_time: int
    notify_times: list
    model_config = SettingsConfigDict(env_file=".env")

class Main:
    def __init__(self):
        self.config = Settings()
        self.tableParser = TableParser(self.config)
        self.telegramBot = TelegramBot(self.config)
        self.chat_ids = set()
        self.lock = threading.Lock()
        threading.Thread(target=self.work, daemon=True).start()

    def is_need_to_notify(self):
        now = datetime.now()
        for i in self.config.notify_times:
            _time = datetime.strptime(i.split()[0], '%H:%M')
            _date = now + timedelta(days={'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5,'Sun':6}[i.split()[-1]] - now.weekday())
            delta = now - datetime(year=_date.year, month=_date.month, day=_date.day, hour=_time.hour, minute=_time.minute)
            if 0 <= delta.total_seconds() < self.config.reboot_time:
                return True
        return False

    def loop(self):
        while True:
            if self.is_need_to_notify():
                phrase = self.tableParser.make_phrase(datetime.now())
                self.lock.acquire()
                for chat_id in self.chat_ids:
                    self.telegramBot.sendMessage(phrase, chat_id)
                self.lock.release()
            time.sleep(self.config.reboot_time)
    
    def work(self):
        for update in self.telegramBot.getUpdates():
            if 'message' in update and 'text' in update['message']:
                chat_id = update['message']['chat']['id']
                text = update['message']['text']
                self.lock.acquire()
                if text == '/start' and chat_id not in self.chat_ids:
                    self.telegramBot.sendMessage('OK Start', chat_id)
                    self.chat_ids.add(chat_id)
                if text == '/stop' and chat_id in self.chat_ids:
                    self.telegramBot.sendMessage('OK Stop', chat_id)
                    self.chat_ids.remove(chat_id)
                self.lock.release()

if __name__ == '__main__':
    Main().loop()