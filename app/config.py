from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongodb_host: str = "fit_galgo_mongodb"
    mongodb_port: int = 27017

    upload_files_folder: str = "files"
    upload_fit_files_folder: str = "files/fit"

    model_config = SettingsConfigDict(env_file=".env")


# # Database configuration
# MONGODB_HOST = "fit_galgo_mongodb"
# MONGODB_PORT = 27017

# # Folder for uploading files
# UPLOAD_FILES_FOLDER = "files"
# UPLOAD_FIT_FILES_FOLDER = os.path.join(UPLOAD_FILES_FOLDER, "fit")
