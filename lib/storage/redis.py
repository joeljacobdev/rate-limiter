from typing import Optional, Any

from redis.asyncio import from_url, Redis

from lib.storage.base import BaseClient


class RedisClient(BaseClient):
    def __init__(self, client_url):
        super().__init__()
        self._client: Redis = from_url(client_url)

    async def increment(self, key) -> int:
        return await self._client.incr(key, 1)

    async def remove_from_list(self, key, value) -> int:
        key_list = await self.get(key) or []
        new_list = list(filter(lambda i: i > value, key_list))
        await self.set(key, data=new_list)
        return len(key_list) - len(new_list)

    async def get(self, key, return_type=int) -> Optional[Any]:
        data = await self._client.get(key)
        if data:
            data = return_type(data)
        return data

    async def release_lock(self, lock):
        pass

    async def set(self, key, data, ttl=None):
        await self._client.setex(key, ttl, data)

    async def get_lock(self, key):
        pass
