from lib.exceptions import rate_limit as rate_limit_exceptions


class LimiterMixin:
    def __init__(self, *args, algorithm=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.algorithm = algorithm

    async def handle_request(self, request):
        key = self.get_key(request)
        if not await self.algorithm.check_rate(key):
            return await self.handle_limit_exceeded(request)

    @staticmethod
    def get_key(request):
        raise NotImplementedError

    async def handle_limit_exceeded(self, request):
        raise rate_limit_exceptions.RateLimited()
