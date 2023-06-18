from typing import Optional
import abc


class StorageResponse:
    def __init__(self, ctr: int, ttl, executed_at):
        self.ctr = ctr
        self.ttl = ttl
        self.executed_at = executed_at


class BaseClient(abc.ABC):
    def __init__(self, storage=None):
        super().__init__()
        self.storage = storage

    @abc.abstractmethod
    async def increment_and_get(self, key, prepare_data) -> StorageResponse:
        pass

    @abc.abstractmethod
    async def get(self, key) -> Optional[StorageResponse]:
        pass
