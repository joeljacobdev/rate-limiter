from typing import Union
from lib.storage import InMemoryClient, StorageResponse

from lib.algorithms.base import BaseAlgorithm


class TokenBucket(BaseAlgorithm):
    """
    Store data as
    {
        'ctr': 0, # no. of times consumed
        'ttl': timestamp # time at which this count will be reset
    }
    """
    async def consume(self, key) -> bool:
        lock = await self.client.get_lock(key)
        await self.refill(key)
        ctr = await self.client.increment(key)
        await self.client.release_lock(lock)
        return ctr <= self.allowed_rate

    async def refill(self, key) -> StorageResponse:
        data = await self.client.get(key)
        if data is None:
            data = self.prepare_data()
        await self.client.set(
            key, data, ttl=self.rate_duration
        )
        return data

    def prepare_data(self) -> Union[int, dict]:
        # TODO: improve this
        if isinstance(self.client, InMemoryClient):
            return {
                'ctr': 0
            }
        return 0
