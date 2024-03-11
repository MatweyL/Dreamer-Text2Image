from pydantic_settings import SettingsConfigDict

from common.settings import SettingsElement


class RabbitMQProducerSettings(SettingsElement):
    reconnect_timeout: int
    produce_retries: int

    model_config = SettingsConfigDict(env_prefix='rabbit_mq_producer_')


class TaskStatusSenderSettings(SettingsElement):
    exchange_name: str
    exchange_type: str
    routing_key: str
    model_config = SettingsConfigDict(env_prefix='task_status_sender_')
