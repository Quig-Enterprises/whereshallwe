from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from pydantic import BaseModel


@dataclass
class Venue:
    id: str
    slug: str
    name: str
    city: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    zip: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    facebook_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    description: Optional[str] = None
    categories: list = field(default_factory=list)
    is_featured: bool = False
    status: str = "active"
    primary_photo: Optional[str] = None
    avg_rating: Optional[float] = None
    rating_count: int = 0
    # wsws-specific
    trail_count: Optional[int] = None
    lift_count: Optional[int] = None
    vertical_drop_ft: Optional[int] = None
    summit_elevation_ft: Optional[int] = None
    base_elevation_ft: Optional[int] = None
    season_opens: Optional[date] = None
    season_closes: Optional[date] = None
    snow_depth_in: Optional[int] = None
    terrain_url: Optional[str] = None


class VenueOut(BaseModel):
    id: str
    slug: str
    name: str
    city: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    zip: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    categories: list[str] = []
    is_featured: bool = False
    avg_rating: Optional[float] = None
    rating_count: int = 0
    primary_photo: Optional[str] = None
    # wsws
    trail_count: Optional[int] = None
    lift_count: Optional[int] = None
    vertical_drop_ft: Optional[int] = None
    snow_depth_in: Optional[int] = None

    class Config:
        from_attributes = True
