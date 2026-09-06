from fastapi import HTTPException, Request

from app.rate_limiter import RateLimiter


rate_limiter = RateLimiter(
    max_requests=5,
    window_seconds=10
)


def check_rate_limit(request: Request):

    client_ip = request.client.host

    allowed, retry_after = rate_limiter.is_allowed(
        client_ip
    )

    if not allowed:

        raise HTTPException(
            status_code=429,
            detail={
                "message": "Rate limit exceeded",
                "retry_after_seconds": retry_after
            },
            headers={
                "Retry-After": str(retry_after)
            }
        )