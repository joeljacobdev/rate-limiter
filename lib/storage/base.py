import abc
from typing import Optional, Any


class StorageResponse:
    def __init__(self, ctr: int):
        self.ctr = ctr

class BaseClient(abc.ABC):
    def __init__(self, storage=None):
        super().__init__()
        self._storage = storage

    @abc.abstractmethod
    async def increment(self, key) -> int:
        pass

    @abc.abstractmethod
    async def remove_from_list(self, key, value) -> int:
        """
        Remove from list stored at :key having values less than :value
        :param key:
        :param value:
        :return: count of element removed from list
        """
        pass

    @abc.abstractmethod
    async def get(self, key) -> Optional[Any]:
        pass

    @abc.abstractmethod
    async def get_lock(self, key):
        pass

    @abc.abstractmethod
    async def set(self, key, data, ttl=None):
        """
        :param key: key on which to store the data
        :param data: data to store
        :param ttl: ttl duration in second
        :return: None
        """
        pass

    @abc.abstractmethod
    async def release_lock(self, lock):
        pass
