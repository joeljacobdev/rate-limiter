import datetime
from typing import Optional

from lib.storage.base import BaseClient, StorageResponse
from lib.utils.lock import LockManager


class InMemoryClient(BaseClient):
    def __init__(self):
        super().__init__()
        self.storage = {}
        self.lock_manager = LockManager()

    async def increment_and_get(self, key, refill_if_needed) -> StorageResponse:
        with self.lock_manager.get_lock(key):
            executed_timestamp = datetime.datetime.now().timestamp()
            data = await refill_if_needed(key)
            data.ctr += 1
            data.executed_at = executed_timestamp
            entry = dict(data.__dict__)
            del entry['executed_at']
            self.storage[key] = entry
        return data

    async def get(self, key, skip_lock=False) -> Optional[StorageResponse]:
        with self.lock_manager.get_lock(key, skip_lock=skip_lock):
            executed_timestamp = datetime.datetime.now().timestamp()
            data = self.storage.get(key)
        if not data:
            return None
        return StorageResponse(**data, executed_at=executed_timestamp)
