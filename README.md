# WhereShallWe

Multi-site venue discovery app serving `whereshallwedance.com` (dance studios/bars) and `whereshallweski.com` (ski resorts) from a single FastAPI application on Alfred.

## Theme System

Each domain resolves to a short theme name (`wswd`, `wsws`) stored in `public.domains.theme_name`. Templates are loaded via Jinja2 `ChoiceLoader`:

1. `app/themes/{theme_name}/` — checked first (per-domain overrides)
2. `app/templates/` — shared fallback (404, 500 in Phase 1)

**Phase 1:** Each theme directory (`wswd/`, `wsws/`) contains complete self-contained templates (`base.html`, `home.html`, `venue.html`, `venues.html`). The ChoiceLoader override mechanism exists for future use — a third domain could override only `home.html` and fall back to shared page templates.

**Cache note:** `app/themes.py` caches the Jinja2 `Environment` per theme name via `lru_cache`. Template changes require `sudo systemctl restart whereshallwe`.

## Database

Single PostgreSQL database `whereshallwe` on Alfred with separate schemas:

- `public.domains` — hostname → site/theme routing
- `wswd.*` — dance venue tables (81 seed venues from whereshallwedance.com)
- `wsws.*` — ski resort tables (17 seed resorts, geocoded)

## Development

```bash
cp .env.example .env
# edit .env with real values
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8091
```

## Tests

```bash
pytest -q
ruff check .
```

## Deployment

Production path: `/var/www/html/whereshallwe/`
Service: `whereshallwe.service` on port 8091

See plan file for full deployment steps (nginx, certbot, DNS flip).
