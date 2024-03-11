from pydantic_settings import BaseSettings, SettingsConfigDict

from common.utils import get_env_path


class SettingsElement(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=get_env_path(),
        env_file_encoding='utf-8',
        extra="ignore"
    )
