import datetime
import threading
from typing import Optional, Any

from lib.storage.base import BaseClient
from lib.utils.lock import LockManager


class InMemoryClient(BaseClient):
    def __init__(self):
        super().__init__()
        self._storage = {}
        self._lock_manager = LockManager()

    async def increment(self, key) -> int:
        data = await self.get(key)
        data['ctr'] += 1
        await self.set(key, data=data)
        return data['ctr']

    async def remove_from_list(self, key, value) -> int:
        key_list = await self.get(key) or []
        new_list = list(filter(lambda i: i > value, key_list))
        await self.set(key, data=new_list)
        return len(key_list) - len(new_list)

    async def get(self, key) -> Optional[Any]:
        data = self._storage.get(key)
        executed_at = datetime.datetime.now().timestamp()
        # implemented ttl logic
        if data and data['ttl'] < executed_at:
            data = None
            del self._storage[key]
        return data

    async def release_lock(self, lock: threading.Lock):
        lock.release()

    async def set(self, key, data, ttl=None):
        if ttl:
            data['ttl'] = (datetime.datetime.now() + datetime.timedelta(seconds=ttl)).timestamp()
        self._storage[key] = data

    async def get_lock(self, key):
        return self._lock_manager.get_lock(key)
