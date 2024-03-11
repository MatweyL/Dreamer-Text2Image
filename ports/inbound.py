from abc import ABC, abstractmethod

from domain.schemas.core.task import FullTaskStatus


class TaskStatusSenderI(ABC):

    @abstractmethod
    async def send(self, task_status: FullTaskStatus):
        pass
