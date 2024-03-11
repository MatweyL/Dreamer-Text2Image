from common.settings import SettingsElement


class RabbitMQProducerSettings(SettingsElement):
    pass


class TaskStatusSenderSettings(SettingsElement):
    pass


rmq_producer_settings = RabbitMQProducerSettings()
task_status_settings = TaskStatusSenderSettings()
