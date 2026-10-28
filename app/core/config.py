from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    APP_NAME: str = "Smart Lock API"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"

    DATABASE_URL: str
    CORS_ORIGINS: list[str] = ["*"]

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()