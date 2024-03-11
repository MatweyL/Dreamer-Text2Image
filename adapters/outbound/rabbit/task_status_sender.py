from domain.schemas.core.task import FullTaskStatus
from ports.outbound import TaskStatusSenderI, RabbitMQProducerI


class RMQTaskStatusSender(TaskStatusSenderI):

    def __init__(self, rabbit_mq_producer: RabbitMQProducerI,
                 exchange_name: str,
                 exchange_type: str,
                 routing_key: str):
        self._rabbit_mq_producer = rabbit_mq_producer
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._routing_key = routing_key

    async def send(self, task_status: FullTaskStatus):
        await self._rabbit_mq_producer.produce(task_status.model_dump(), self._exchange_name, self._exchange_type,
                                               self._routing_key, None)
