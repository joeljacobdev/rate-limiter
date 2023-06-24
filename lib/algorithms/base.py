from lib.storage.base import BaseClient


class BaseAlgorithm:
    def __init__(self, client: BaseClient, allowed_rate=10, rate_duration=60, **kwargs):
        super().__init__(**kwargs)
        self.client = client
        self.allowed_rate = allowed_rate
        self.rate_duration = rate_duration

    async def check_rate(self, key) -> bool:
        raise NotImplementedError

    def prepare_data(self):
        raise NotImplementedError
