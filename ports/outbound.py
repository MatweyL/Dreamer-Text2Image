from abc import ABC, abstractmethod

from pydantic import BaseModel

from domain.schemas.core.task import FullTaskStatus


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
