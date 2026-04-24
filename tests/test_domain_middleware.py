"""Tests for DomainMiddleware."""
import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault("DATABASE_URL", "postgresql://fake/fake")
os.environ.setdefault("SECRET_KEY", "test-secret-key-long-enough-for-tests-ok")
os.environ.setdefault("APP_ENV", "development")

from app.middleware.domain import DomainMiddleware, _cache, _cache_set  # noqa: E402
from app.models.domain import DomainConfig  # noqa: E402


def _make_domain_config(hostname="whereshallwedance.com") -> DomainConfig:
    return DomainConfig(
        id="test-id",
        hostname=hostname,
        site="wswd",
        theme_name="wswd",
        site_name="Where Shall We Dance",
        is_active=True,
    )


def _make_request(hostname: str, path: str = "/") -> MagicMock:
    req = MagicMock()
    req.headers = {"host": hostname}
    req.url.path = path
    req.state = MagicMock()
    return req


@pytest.mark.asyncio
async def test_known_active_domain_sets_state():
    """Known active domain sets request.state.domain and .theme."""
    config = _make_domain_config()
    _cache.clear()
    _cache_set("whereshallwedance.com", config)

    middleware = DomainMiddleware(app=AsyncMock())
    req = _make_request("whereshallwedance.com")

    call_next = AsyncMock(return_value=MagicMock(status_code=200))
    await middleware.dispatch(req, call_next)

    assert req.state.domain.theme_name == "wswd"
    assert req.state.theme == "wswd"


@pytest.mark.asyncio
async def test_unknown_domain_returns_404():
    """Unknown hostname returns a 404 JSON response."""
    _cache.clear()
    _cache_set("unknown-host.example.com", None)

    middleware = DomainMiddleware(app=AsyncMock())
    req = _make_request("unknown-host.example.com")

    call_next = AsyncMock(return_value=MagicMock(status_code=200))
    response = await middleware.dispatch(req, call_next)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_inactive_domain_returns_404():
    """Inactive domain returns 404."""
    config = DomainConfig(
        id="id2", hostname="inactive.example.com", site="wswd",
        theme_name="wswd", site_name="Test", is_active=False,
    )
    _cache.clear()
    _cache_set("inactive.example.com", config)

    middleware = DomainMiddleware(app=AsyncMock())
    req = _make_request("inactive.example.com")
    call_next = AsyncMock(return_value=MagicMock(status_code=200))
    response = await middleware.dispatch(req, call_next)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_bypass_path_skips_domain_lookup():
    """/health path bypasses domain resolution."""
    _cache.clear()

    middleware = DomainMiddleware(app=AsyncMock())
    req = _make_request("any-host.example.com", path="/health")
    call_next = AsyncMock(return_value=MagicMock(status_code=200))
    await middleware.dispatch(req, call_next)

    assert req.state.domain is None
    call_next.assert_called_once()
