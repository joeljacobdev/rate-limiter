import uvicorn
from fastapi import FastAPI
from lib import LimiterMixin, TokenBucket, InMemoryClient
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


class LimiterMiddleware(LimiterMixin, BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        await self.handle_request(request)
        return await call_next(request)

    @staticmethod
    def get_key(request):
        return request.scope['path']


@app.get("/")
async def index():
    return {"message": "Hello, World!"}


app.add_middleware(
    LimiterMiddleware,
    algorithm=TokenBucket(client=InMemoryClient())
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)