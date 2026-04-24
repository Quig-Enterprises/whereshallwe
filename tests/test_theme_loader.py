"""Tests for the ChoiceLoader theme system."""
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock


# Ensure the project root is importable without needing .env
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Stub out config before import so SECRET_KEY guard doesn't fire
os.environ.setdefault("DATABASE_URL", "postgresql://fake/fake")
os.environ.setdefault("SECRET_KEY", "test-secret-key-long-enough-for-tests-ok")
os.environ.setdefault("APP_ENV", "development")

from app.themes import _get_env, render  # noqa: E402


def _make_request(theme: str = "wswd") -> MagicMock:
    req = MagicMock()
    req.state.theme = theme
    req.url_for.return_value = "/static/shared/reset.css"
    return req


def test_get_env_wswd_resolves_base():
    """ChoiceLoader finds base.html in wswd theme directory."""
    env = _get_env("wswd")
    tpl = env.get_template("base.html")
    assert tpl is not None


def test_get_env_wsws_resolves_base():
    """ChoiceLoader finds base.html in wsws theme directory."""
    env = _get_env("wsws")
    tpl = env.get_template("base.html")
    assert tpl is not None


def test_fallback_to_shared_404():
    """ChoiceLoader falls back to shared templates/404.html."""
    env = _get_env("wswd")
    tpl = env.get_template("404.html")
    assert tpl is not None
    # 404 template exists in shared templates/ not wswd/
    assert env is not None


def test_cache_returns_same_instance():
    """Same theme_name returns the same cached Environment (lru_cache)."""
    env1 = _get_env("wswd")
    env2 = _get_env("wswd")
    assert env1 is env2


def test_wswd_and_wsws_are_separate_envs():
    """Different theme names return different Environment instances."""
    env_wswd = _get_env("wswd")
    env_wsws = _get_env("wsws")
    assert env_wswd is not env_wsws


def test_render_returns_html_response():
    """render() returns an HTMLResponse with content."""
    req = _make_request("wswd")
    req.state.domain = MagicMock()
    req.state.domain.site_name = "Where Shall We Dance"

    response = render(req, "404.html", {})
    from fastapi.responses import HTMLResponse
    assert isinstance(response, HTMLResponse)
    assert b"404" in response.body
