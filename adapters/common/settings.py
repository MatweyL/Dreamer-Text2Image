from typing import Optional

from pydantic_settings import SettingsConfigDict

from common.settings import SettingsElement


class RabbitMQConnectionSettings(SettingsElement):
    protocol: str = "ampq"
    host: str
    port: Optional[int] = 5672
    user: str
    password: str
    virtual_host: str = "/"

    model_config = SettingsConfigDict(env_prefix='rabbit_mq_connection_')
