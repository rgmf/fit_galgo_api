from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongodb_host: str = "fit_galgo_mongodb"
    mongodb_port: int = 27017

    upload_files_folder: str = "files"
    upload_fit_files_folder: str = "files/fit"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
