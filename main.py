import uvicorn
from fastapi import FastAPI, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from lib import LimiterMixin, TokenBucket, RedisClient, RateLimited

app = FastAPI()


class LimiterMiddleware(LimiterMixin, BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            await self.handle_request(request)
        except RateLimited:
            return Response(status_code=status.HTTP_429_TOO_MANY_REQUESTS)
        return await call_next(request)

    @staticmethod
    def get_key(request):
        return request.scope['path']


@app.get("/")
async def index():
    return {"message": "Hello, World!"}


app.add_middleware(
    LimiterMiddleware,
    algorithm=TokenBucket(client=RedisClient(client_url='redis://localhost:9500/1')),
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
