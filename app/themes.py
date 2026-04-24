from functools import lru_cache
from pathlib import Path

from fastapi.responses import HTMLResponse
from fastapi import Request
from jinja2 import ChoiceLoader, Environment, FileSystemLoader

BASE_DIR = Path(__file__).resolve().parent


@lru_cache(maxsize=32)
def _get_env(theme_name: str) -> Environment:
    # lru_cache keyed on theme_name — stale if template files change on disk.
    # Cache invalidation: `sudo systemctl restart whereshallwe`
    loader = ChoiceLoader([
        FileSystemLoader(str(BASE_DIR / "themes" / theme_name)),
        FileSystemLoader(str(BASE_DIR / "templates")),
    ])
    return Environment(loader=loader, autoescape=True)


def render(request: Request, template_name: str, context: dict) -> HTMLResponse:
    theme_name = getattr(request.state, "theme", "default")
    env = _get_env(theme_name)
    template = env.get_template(template_name)
    content = template.render({"request": request, **context})
    return HTMLResponse(content=content)
