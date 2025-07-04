import datetime, time, threading
from pydantic_settings import BaseSettings, SettingsConfigDict
from TableParser import TableParser
from TelegramBot import TelegramBot

class Settings(BaseSettings):
    api_token: str
    table_path: str
    reasons_location: str
    reasons_count: int
    dba_count: int
    reboot_time: int
    notify_times: str
    model_config = SettingsConfigDict(env_file=".env")

class Main:
    def __init__(self):
        self.config = Settings()
        self.tableParser = TableParser(self.config)
        self.telegramBot = TelegramBot(self.config)
        self.chat_ids = set()
        self.lock = threading.Lock()
        threading.Thread(target=self.work, daemon=True).start()

    def loop(self):
        while True:
            pass
    
    def work(self):
        for update in self.telegramBot.getUpdates():
            print(update)
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

Main().loop()