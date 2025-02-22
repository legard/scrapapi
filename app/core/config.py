from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "ScrapAPI"
    API_V1_STR: str = "/api/v1"
    REDIS_URL: str = "redis://redis:6379"

    HTTP_PROXY: str | None = None
    HTTPS_PROXY: str | None = None

    class Config:
        case_sensitive = True


settings = Settings()
