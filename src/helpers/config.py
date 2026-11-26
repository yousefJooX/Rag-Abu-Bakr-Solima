"""Load the configuration required to run Mini RAG."""

from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    """Define the app's identity, provider credentials, upload limits, and database settings."""

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
        """Read UTF-8 .env values and match environment variable names by case."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

def get_settings():
    """Load settings and validate the required values from the environment and .env."""
    return Settings()
