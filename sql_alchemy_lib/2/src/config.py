from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

# Загрузка переменных из .env файла
load_dotenv()

class Settings(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST",)
    DB_PORT: int = int(os.getenv("DB_PORT",))
    DB_USER: str = os.getenv("DB_USER",)
    DB_PASS: str = os.getenv("DB_PASS",)
    DB_NAME: str = os.getenv("DB_NAME",)

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

# Проверка значений
#print(settings.DB_HOST)
#print(settings.DATABASE_URL_asyncpg)
