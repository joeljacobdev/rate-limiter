
class RateLimited(Exception):
    status_code = 429
    message = "Rate Limited"
