from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Cinema API"

    DATABASE_URL: str = "sqlite:///./cinema.db"

    REDIS_URL: str | None = None

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    REDIS_HOST: str = "localhost"

    REDIS_PORT: int = 6379

    REDIS_DB: int = 0

    CLOUDINARY_CLOUD_NAME: str

    CLOUDINARY_API_KEY: str
    
    CLOUDINARY_API_SECRET: str

    model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    )


settings = Settings()