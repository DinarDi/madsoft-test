from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Основные настройки приложения
    """
    model_config = SettingsConfigDict(
        env_file='.env.app',
        extra='allow',
    )
    DB_URL: str
    MEDIA_URL: str


settings = Settings()
