from pydantic_settings import BaseSettings
class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    AUTHOR: str
    OPENAI_API_KEY: str
    NVIDIA_API_KEY: str
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE_MB: int
    FILE_DEFAULT_CHUNK_SIZE: int
    MONGO_URI: str
    MONGO_DATABASE: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

def get_settings():
    return Settings()
