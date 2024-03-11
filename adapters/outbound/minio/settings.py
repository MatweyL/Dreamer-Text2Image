from pydantic_settings import SettingsConfigDict

from common.settings import SettingsElement


class MinioSettings(SettingsElement):
    host: str
    user: str
    password: str
    bucket: str
    retries: int
    retry_timeout: int

    model_config = SettingsConfigDict(env_prefix='minio_')

