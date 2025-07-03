import datetime
from pydantic_settings import BaseSettings, SettingsConfigDict
from TableParser import TableParser

class Settings(BaseSettings):
    api_token: str
    table_path: str
    reasons_location: str
    reasons_count: str
    reboot_time: int
    notify_times: str
    model_config = SettingsConfigDict(env_file=".env")

s = Settings()
TableParser(s)