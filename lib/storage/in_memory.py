import datetime
import threading
from typing import Optional

from lib.storage.base import BaseClient, StorageResponse


class InMemoryClient(BaseClient):
    def __init__(self):
        super().__init__()
        self.storage = {}
        self.lock = threading.Lock()

    async def increment_and_get(self, key, prepare_data) -> StorageResponse:
        with self.lock:
            executed_timestamp = datetime.datetime.now().timestamp()
            data = self.storage.get(key)
            if not data:
                data = prepare_data()
            elif executed_timestamp > data['ttl']:
                data = prepare_data()
            data['ctr'] += 1
            self.storage[key] = data
        return StorageResponse(**data, executed_at=executed_timestamp)

    async def get(self, key) -> Optional[StorageResponse]:
        with self.lock:
            executed_timestamp = datetime.datetime.now().timestamp()
            data = self.storage.get(key)
        if not data:
            return None
        return StorageResponse(**data, executed_at=executed_timestamp)
