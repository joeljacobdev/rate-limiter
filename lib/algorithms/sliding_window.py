import datetime

from lib.algorithms.base import BaseAlgorithm


# TODO: WIP
class SlidingWindow(BaseAlgorithm):
    async def consume(self, key) -> bool:
        ctr = await self.client.increment(key)
        return ctr < self.allowed_rate

    async def refill(self, key):
        data = await self.client.get(key)
        executed_at = datetime.datetime.now()
        if not data or data.ctr > self.allowed_rate:
            cutoff_time = executed_at - datetime.timedelta(seconds=self.rate_duration)
            removed = self.client.remove_from_list(f'{key}_list', cutoff_time)
            data.ctr -= removed

    def prepare_data(self):
        return {
            'ctr': 0,
            'logs': (datetime.datetime.now() + datetime.timedelta(seconds=self.rate_duration)).timestamp()
        }