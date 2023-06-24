import datetime

from lib.algorithms.base import BaseAlgorithm
from lib.storage.base import StorageResponse


class TokenBucket(BaseAlgorithm):
    """
    Store data as
    {
        'ctr': 0, # no. of times consumed
        'ttl': timestamp # time at which this count will be reset
    }
    """
    async def consume(self, key) -> bool:
        data = await self.client.increment_and_get(key, refill_if_needed=self.refill)
        return data.ctr < self.allowed_rate

    async def refill(self, key) -> StorageResponse:
        data = await self.client.get(key, skip_lock=True)
        executed_at = datetime.datetime.now().timestamp()
        if not data or data.ttl < executed_at:
            data = self.prepare_data()
            data = StorageResponse(**data)
        data.executed_at = executed_at
        return data

    def prepare_data(self):
        return {
            'ctr': 0,
            'ttl': (datetime.datetime.now() + datetime.timedelta(seconds=self.rate_duration)).timestamp()
        }