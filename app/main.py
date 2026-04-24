from contextlib import asynccontextmanager
import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.db import close_pool, init_pool
from app.middleware.cors import DynamicCORSMiddleware
from app.middleware.domain import DomainMiddleware
from app.middleware.rate_limit import limiter
from app.routers import health, pages, api

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool(settings.DATABASE_URL)
    yield
    await close_pool()


app = FastAPI(
    title="WhereShallWe",
    version="0.1.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        if request.headers.get("x-forwarded-proto", "http") == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://api.mapbox.com https://events.mapbox.com "
            "https://cdn.jsdelivr.net https://static.cloudflareinsights.com; "
            "style-src 'self' 'unsafe-inline' https://api.mapbox.com https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: blob: https://api.mapbox.com *.mapbox.com; "
            "connect-src 'self' https://api.mapbox.com https://events.mapbox.com; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        return response


app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(DynamicCORSMiddleware)
app.add_middleware(DomainMiddleware)

app.include_router(health.router)
app.include_router(pages.router, tags=["pages"])
app.include_router(api.router, prefix="/api", tags=["api"])


@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap(request: Request):
    scheme = request.headers.get("x-forwarded-proto", "https")
    host = request.headers.get("host", "localhost")
    base_url = f"{scheme}://{host}"

    pages_list = ["/", "/venues", "/map", "/about", "/contact"]
    urls = "\n".join(f"  <url><loc>{base_url}{p}</loc></url>" for p in pages_list)
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>"""
    return Response(content=xml, media_type="application/xml")


app.mount("/static", StaticFiles(directory=BASE_DIR.parent / "static"), name="static")
