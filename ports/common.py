from abc import ABC, abstractmethod
from typing import Any


class Startable(ABC):

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass


class ConverterI(ABC):

    @abstractmethod
    def convert(self, data: Any) -> Any:
        pass
