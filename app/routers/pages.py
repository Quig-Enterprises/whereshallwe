from collections import defaultdict
from typing import Optional

from fastapi import APIRouter, Request

from app.config import settings
from app.db import get_pool
from app.routers.api import _STATE_ABBR
from app.themes import render

router = APIRouter()


async def _list_venues(pool, site: str, *, q: str = None, city: str = None,
                       state: str = None, category: str = None,
                       featured_only: bool = False, limit: int = 200) -> list:
    conditions = ["status = 'active'"]
    params = []

    if featured_only:
        conditions.append("is_featured = true")

    if q:
        params.append(f"%{q.lower()}%")
        conditions.append(f"(lower(name) LIKE ${len(params)} OR lower(city) LIKE ${len(params)})")

    if city:
        params.append(f"%{city.lower()}%")
        conditions.append(f"lower(city) LIKE ${len(params)}")

    if state:
        state_val = _STATE_ABBR.get(state.upper(), state)
        params.append(state_val)
        params.append(state.upper())
        conditions.append(f"(state = ${len(params) - 1} OR state = ${len(params)})")

    if category:
        params.append(category)
        conditions.append(f"${len(params)} = ANY(categories)")

    where = " AND ".join(conditions)
    params.append(limit)
    sql = f"SELECT * FROM {site}.venues WHERE {where} ORDER BY is_featured DESC, name ASC LIMIT ${len(params)}"

    async with pool.acquire() as conn:
        rows = await conn.fetch(sql, *params)
    return [dict(r) for r in rows]


@router.get("/")
async def home(request: Request):
    pool = get_pool()
    site = request.state.domain.site if request.state.domain else "wswd"
    featured = []
    venues_by_state = {}

    if pool:
        featured = await _list_venues(pool, site, featured_only=True, limit=8)
        if site == "wsws":
            all_venues = await _list_venues(pool, site)
            by_state = defaultdict(list)
            for v in all_venues:
                by_state[v["state"] or "Other"].append(v)
            venues_by_state = dict(sorted(by_state.items()))

    return render(request, "home.html", {
        "featured": featured,
        "venues_by_state": venues_by_state,
        "page": "home",
    })


@router.get("/venues")
async def venues_list(
    request: Request,
    q: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    category: Optional[str] = None,
):
    pool = get_pool()
    site = request.state.domain.site if request.state.domain else "wswd"
    venues = []

    if pool:
        venues = await _list_venues(pool, site, q=q, city=city, state=state, category=category)

    return render(request, "venues.html", {
        "venues": venues,
        "q": q,
        "city": city,
        "state": state,
        "category": category,
        "page": "venues",
    })


@router.get("/venue/{slug}")
async def venue_detail(request: Request, slug: str):
    pool = get_pool()
    site = request.state.domain.site if request.state.domain else "wswd"

    if pool:
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                f"SELECT * FROM {site}.venues WHERE slug = $1", slug
            )
            conditions = []
            if row and site == "wsws":
                crows = await conn.fetch(
                    "SELECT * FROM wsws.venue_conditions WHERE venue_id = $1 ORDER BY reported_at DESC LIMIT 12",
                    row["id"],
                )
                conditions = [dict(r) for r in crows]

        if not row:
            return render(request, "404.html", {})

        return render(request, "venue.html", {
            "venue": dict(row),
            "conditions": conditions if site == "wsws" else [],
            "page": "venue",
        })

    return render(request, "venue.html", {"venue": {}, "conditions": [], "page": "venue"})


@router.get("/map")
async def map_page(request: Request):
    pool = get_pool()
    site = request.state.domain.site if request.state.domain else "wswd"
    venues = []

    if pool:
        extra_col = ", snow_depth_in" if site == "wsws" else ""
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                f"SELECT id, slug, name, city, state, lat, lng, categories{extra_col} "
                f"FROM {site}.venues "
                "WHERE status = 'active' AND lat IS NOT NULL AND lng IS NOT NULL"
            )
        venues = []
        for r in rows:
            v = dict(r)
            v["id"] = str(v["id"])
            if v.get("lat") is not None:
                v["lat"] = float(v["lat"])
            if v.get("lng") is not None:
                v["lng"] = float(v["lng"])
            venues.append(v)

    return render(request, "map.html", {
        "venues": venues,
        "mapbox_token": settings.MAPBOX_TOKEN,
        "page": "map",
    })


@router.get("/about")
async def about(request: Request):
    return render(request, "venues.html", {"venues": [], "page": "about",
                                            "q": None, "city": None, "state": None, "category": None})


@router.get("/contact")
async def contact(request: Request):
    return render(request, "venues.html", {"venues": [], "page": "contact",
                                            "q": None, "city": None, "state": None, "category": None})
