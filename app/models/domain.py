from dataclasses import dataclass
from typing import Literal


@dataclass
class DomainConfig:
    id: str
    hostname: str
    site: Literal["wswd", "wsws"]
    theme_name: str
    site_name: str
    is_active: bool

    @classmethod
    def from_record(cls, row) -> "DomainConfig":
        return cls(
            id=str(row["id"]),
            hostname=row["hostname"],
            site=row["site"],
            theme_name=row["theme_name"],
            site_name=row["site_name"],
            is_active=row["is_active"],
        )
