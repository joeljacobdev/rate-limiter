import datetime

from lib.algorithms.base import BaseAlgorithm


class SlidingWindow(BaseAlgorithm):
    async def check_rate(self, key) -> bool:
        data = await self.client.increment_and_get(key, prepare_data=self.prepare_data)
        return data.ctr < self.allowed_rate

    def prepare_data(self):
        return {
            'ctr': 0,
            'ttl': (datetime.datetime.now() + datetime.timedelta(seconds=self.rate_duration)).timestamp()
        }