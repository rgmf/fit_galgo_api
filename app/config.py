import os

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongodb_host: str
    mongodb_port: int

    upload_files_folder: str
    upload_fit_files_folder: str
    upload_zip_files_folder: str
    upload_tmp_files_folder: str

    secret_key: str

    #model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), '..', '.env'))
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
