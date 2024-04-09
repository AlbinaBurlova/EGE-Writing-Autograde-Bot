from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr
    developer_id_1: int
    developer_id_2: int
    api_address: SecretStr
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8')


config = Settings()
