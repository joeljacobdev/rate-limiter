from fastapi import FastAPI
from lib.limiter import LimiterMixin
from lib.algorithms.base import TokenBucket
from lib.storage.in_memory import InMemoryClient
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


class LimiterMiddleware(LimiterMixin, BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        await self.handle_request(request)
        return await call_next(request)

    @staticmethod
    def get_key(request):
        raise request.scope['path']


@app.get("/")
async def index():
    return {"message": "Hello, World!"}


app.add_middleware(
    LimiterMiddleware,
    algorithm=TokenBucket(client=InMemoryClient())
)
