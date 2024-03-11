from abc import ABC, abstractmethod


class ObjectStorageI(ABC):

    @abstractmethod
    def save(self, name: str, obj: bytes):
        pass
