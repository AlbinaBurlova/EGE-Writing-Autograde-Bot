from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    bot_token: SecretStr
    developer_id_1: int
    developer_id_2: int
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
