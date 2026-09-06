from fastapi import Request
from fastapi.responses import JSONResponse

from app.rate_limiter import RateLimiter


rate_limiter = RateLimiter(
    max_requests=5,
    window_seconds=10
)


async def rate_limit_middleware(request: Request, call_next):

    client_ip = request.client.host

    allowed, retry_after = rate_limiter.is_allowed(
        client_ip
    )

    if not allowed:

        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded",
                "retry_after_seconds": retry_after
            },
            headers={
                "Retry-After": str(retry_after)
            }
        )

    response = await call_next(request)

    return response