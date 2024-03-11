from pydantic_settings import BaseSettings, SettingsConfigDict

from common.utils import get_env_path


class ConfigCollector:
    configurations = dict()

    def __init__(self):
        config_name = self.model_config.get("env_prefix", "base").strip("_")
        self.__class__.configurations[config_name] = self

    @classmethod
    def get_all(cls):
        return cls.configurations


class SettingsElement(ConfigCollector, BaseSettings):
    def __init__(self, *args, **kwargs):
        ConfigCollector.__init__(self)
        BaseSettings.__init__(self, *args, **kwargs)

    model_config = SettingsConfigDict(
        env_file=get_env_path(),
        env_file_encoding='utf-8',
        extra="ignore"
    )
