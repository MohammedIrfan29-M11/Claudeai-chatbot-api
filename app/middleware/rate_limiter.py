import logging
import time
from collections import defaultdict
from fastapi import Request,HTTPException

logger = logging.getLogger('app.middleware')

request_counts: dict[str, list] = defaultdict(list)

async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware runs on EVERY request before it reaches your route.
    Think of it as a security guard at the door — checks everyone
    before letting them into the building.

    call_next is the rest of the application — we call it to
    continue processing the request if it passes our check.
    """

    if request.url.path in ["/chat", "chat/stream"]:
        client_ip = request.headers.get("X-Forwarded-For", request.client.host)

        now = time.time()

        request_counts[client_ip] = [
            timestamp for timestamp in request_counts[client_ip]
            if now - timestamp < 60
            ]

        if len(request_counts[client_ip]) >= 10:
            logger.warning(
                f"Rate limit exceeded for IP: {client_ip} | "
                f"Requests: {len(request_counts[client_ip])}"
            )
            raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")

        request_counts[client_ip].append(now)

        logger.debug(
            f"Requests allowed for IP: {client_ip} | "
            f"count: {len(request_counts[client_ip])}"
        )

    response = await call_next(request)
    return response
