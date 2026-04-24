import logging
import time
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.db import get_pool
from app.models.domain import DomainConfig

logger = logging.getLogger(__name__)

_cache: dict[str, tuple[Optional[DomainConfig], float]] = {}
_CACHE_TTL = 60.0
_MAX_CACHE_SIZE = 200


def _cache_get(hostname: str) -> tuple[bool, Optional[DomainConfig]]:
    entry = _cache.get(hostname)
    if entry is None:
        return False, None
    config, ts = entry
    if time.monotonic() - ts > _CACHE_TTL:
        del _cache[hostname]
        return False, None
    return True, config


def _cache_set(hostname: str, config: Optional[DomainConfig]) -> None:
    if len(_cache) >= _MAX_CACHE_SIZE and hostname not in _cache:
        oldest = min(_cache, key=lambda k: _cache[k][1])
        del _cache[oldest]
    _cache[hostname] = (config, time.monotonic())


_BYPASS_PATHS = frozenset(["/health", "/sitemap.xml"])


class DomainMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in _BYPASS_PATHS:
            request.state.domain = None
            request.state.theme = "default"
            return await call_next(request)

        raw_host = request.headers.get("host", "")
        hostname = raw_host.split(":")[0].lower()

        hit, cached_config = _cache_get(hostname)

        if not hit:
            pool = get_pool()
            if pool is None:
                request.state.domain = None
                request.state.theme = "default"
                return await call_next(request)

            try:
                async with pool.acquire() as conn:
                    row = await conn.fetchrow(
                        "SELECT * FROM public.domains WHERE hostname = $1 AND is_active = true",
                        hostname,
                    )
                config = DomainConfig.from_record(row) if row else None
            except Exception as exc:
                logger.error(
                    "domain_lookup_failed domain=%s error=%s: %s",
                    hostname,
                    type(exc).__name__,
                    exc,
                    exc_info=True,
                )
                config = None

            _cache_set(hostname, config)
        else:
            config = cached_config

        if config is None or not config.is_active:
            return JSONResponse(
                status_code=404,
                content={"detail": "Domain not configured"},
            )

        request.state.domain = config
        request.state.theme = config.theme_name
        return await call_next(request)
