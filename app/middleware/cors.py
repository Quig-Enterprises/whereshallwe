"""Dynamic CORS middleware — loads allowed origins from the domains table.

Origins are lazily loaded on first request and cached for 5 minutes.
The cache is never cleared on DB error to avoid disrupting live traffic.
"""
import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.db import get_pool

logger = logging.getLogger(__name__)

_CORS_CACHE_TTL = 300.0  # seconds
_allowed_origins: set[str] = set()
_last_loaded: float = 0.0

_CORS_METHODS = "GET, POST, PUT, DELETE, OPTIONS"
_CORS_HEADERS = "Content-Type, Authorization"


async def _load_origins() -> set[str]:
    pool = get_pool()
    if pool is None:
        return set()
    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT hostname FROM public.domains")
        origins: set[str] = set()
        for row in rows:
            h = row["hostname"].lower().strip()
            origins.add(f"https://{h}")
            origins.add(f"https://www.{h}")
        return origins
    except Exception as exc:
        logger.error("cors_origin_load_failed: %s", exc, exc_info=True)
        return set()


class DynamicCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        global _allowed_origins, _last_loaded

        now = time.monotonic()
        if now - _last_loaded > _CORS_CACHE_TTL:
            fresh = await _load_origins()
            if fresh:
                _allowed_origins = fresh
            _last_loaded = now

        origin = request.headers.get("origin", "")
        allowed = origin and origin in _allowed_origins

        if request.method == "OPTIONS" and allowed:
            response = Response(status_code=204)
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = _CORS_METHODS
            response.headers["Access-Control-Allow-Headers"] = _CORS_HEADERS
            response.headers["Access-Control-Max-Age"] = "600"
            response.headers["Vary"] = "Origin"
            return response

        response = await call_next(request)

        if allowed:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = _CORS_METHODS
            response.headers["Access-Control-Allow-Headers"] = _CORS_HEADERS
            response.headers["Vary"] = "Origin"

        return response
