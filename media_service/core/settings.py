from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class MediaServiceSettings(BaseSettings):
    """
    Основные настройки приложения
    """
    model_config = SettingsConfigDict(
        env_file='.env.app',
        extra='allow',
    )
    ENDPOINT: str
    MINIO_SERVER_ACCESS_KEY: str
    MINIO_SERVER_SECRET_KEY: str
    BUCKET: str


media_settings = MediaServiceSettings()
