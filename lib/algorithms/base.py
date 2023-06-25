from lib.storage.base import BaseClient


class BaseAlgorithm:
    def __init__(self, client: BaseClient, allowed_rate=10, rate_duration=60, **kwargs):
        super().__init__(**kwargs)
        self.client = client
        self.allowed_rate = allowed_rate
        self.rate_duration = rate_duration

    async def consume(self, key) -> bool:
        """
        Return true if capacity is consumed for the :key.
        Takes lock, refill if criteria met and then increment count and finally releases lock
        :param key:
        :return: boolean, True if consumed else False
        """
        raise NotImplementedError

    async def refill(self, key):
        raise NotImplementedError

    def prepare_data(self) -> dict:
        """
        Initial data to be stored for a key
        :return: dict
        """
        raise NotImplementedError
