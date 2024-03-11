from abc import ABC, abstractmethod

from pydantic import BaseModel

from domain.schemas.core.task import FullTaskStatus
from ports.common import Startable


class SavedObject(BaseModel):
    url: str


class ObjectStorageI(ABC):

    @abstractmethod
    async def save(self, name: str, obj: bytes) -> SavedObject:
        pass


class TaskStatusSenderI(ABC):

    @abstractmethod
    async def send(self, task_status: FullTaskStatus):
        pass


class RabbitMQProducerI(Startable, ABC):

    @abstractmethod
    async def produce(self, data: dict, exchange_name: str, exchange_type: str, routing_key: str, headers: dict):
        pass
