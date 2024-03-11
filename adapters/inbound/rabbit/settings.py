from pydantic_settings import SettingsConfigDict

from common.settings import SettingsElement


class RabbitMQConsumerSettings(SettingsElement):
    queue_name: str
    prefetch_count: int
    reconnect_timeout: int

    model_config = SettingsConfigDict(env_prefix='rabbit_mq_consumer_')
