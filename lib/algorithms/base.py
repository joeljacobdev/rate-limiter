import datetime
from typing import Type

from lib.storage.base import BaseClient


class TokenBucket:
    def __init__(self, client: BaseClient, allowed_rate=10, rate_duration=60, **kwargs):
        super().__init__(**kwargs)
        self.client = client
        self.allowed_rate = allowed_rate
        self.rate_duration = rate_duration

    async def check_rate(self, key) -> bool:
        data = await self.client.increment_and_get(key, prepare_data=self.prepare_data)
        return data.ctr < self.allowed_rate

    def prepare_data(self):
        return {
            'ctr': 0,
            'ttl': (datetime.datetime.now() + datetime.timedelta(seconds=self.rate_duration)).timestamp()
        }
