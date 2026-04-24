from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.db import get_pool

router = APIRouter()

_MAX_PER_PAGE = 100

# Maps 2-letter state abbreviation -> full state name as stored in seed data
_STATE_ABBR = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming",
}


async def _query_venues(pool, site: str, *, q=None, state=None, city=None,
                        category=None, page: int = 1, per_page: int = 50) -> tuple:
    conditions = ["status = 'active'"]
    params = []

    if q:
        params.append(f"%{q.lower()}%")
        conditions.append(f"(lower(name) LIKE ${len(params)} OR lower(city) LIKE ${len(params)})")

    if state:
        # Accept both abbreviations ("FL") and full names ("Florida")
        state_val = _STATE_ABBR.get(state.upper(), state)
        params.append(state_val)
        params.append(state.upper())
        conditions.append(f"(state = ${len(params) - 1} OR state = ${len(params)})")

    if city:
        params.append(f"%{city.lower()}%")
        conditions.append(f"lower(city) LIKE ${len(params)}")

    if category:
        params.append(category)
        conditions.append(f"${len(params)} = ANY(categories)")

    where = " AND ".join(conditions)
    offset = (page - 1) * per_page

    params.extend([per_page, offset])
    sql = (
        f"SELECT * FROM {site}.venues WHERE {where} "
        f"ORDER BY is_featured DESC, name ASC "
        f"LIMIT ${len(params) - 1} OFFSET ${len(params)}"
    )

    count_sql = f"SELECT COUNT(*) FROM {site}.venues WHERE {where}"

    async with pool.acquire() as conn:
        rows = await conn.fetch(sql, *params[:-2], per_page, offset)
        total = await conn.fetchval(count_sql, *params[:-2])

    return [dict(r) for r in rows], total


def _serialize(row: dict) -> dict:
    result = {}
    for k, v in row.items():
        if hasattr(v, "isoformat"):
            result[k] = v.isoformat()
        elif isinstance(v, (str, int, float, bool, list, type(None))):
            result[k] = v
        else:
            result[k] = str(v)
    return result


@router.get("/venues")
async def api_venues(
    request: Request,
    q: Optional[str] = None,
    state: Optional[str] = None,
    city: Optional[str] = None,
    category: Optional[str] = None,
    page: int = 1,
    per_page: int = 50,
):
    per_page = min(per_page, _MAX_PER_PAGE)
    pool = get_pool()
    site = request.state.domain.site if request.state.domain else "wswd"

    if not pool:
        return JSONResponse({"venues": [], "total": 0, "page": page, "per_page": per_page})

    rows, total = await _query_venues(
        pool, site, q=q, state=state, city=city, category=category,
        page=page, per_page=per_page,
    )
    return JSONResponse({
        "venues": [_serialize(r) for r in rows],
        "total": total,
        "page": page,
        "per_page": per_page,
    })


@router.get("/venues/{slug}")
async def api_venue_detail(request: Request, slug: str):
    pool = get_pool()
    site = request.state.domain.site if request.state.domain else "wswd"

    if not pool:
        return JSONResponse({"detail": "unavailable"}, status_code=503)

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            f"SELECT * FROM {site}.venues WHERE slug = $1", slug
        )

    if not row:
        return JSONResponse({"detail": "not found"}, status_code=404)

    return JSONResponse(_serialize(dict(row)))
