import abc
from typing import Optional


class StorageResponse:
    def __init__(self, ctr: int, ttl, executed_at=None):
        self.ctr = ctr
        self.ttl = ttl
        self.executed_at = executed_at


class BaseClient(abc.ABC):
    def __init__(self, storage=None):
        super().__init__()
        self.storage = storage

    @abc.abstractmethod
    async def increment_and_get(self, key, refill_if_needed) -> StorageResponse:
        pass

    @abc.abstractmethod
    async def get(self, key, skip_lock=False) -> Optional[StorageResponse]:
        pass
