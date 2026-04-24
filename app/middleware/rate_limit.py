"""Rate limiting via slowapi (in-memory, per-worker).

Note: with 2 uvicorn workers, effective limit is 2x the nominal value.
Key function reads X-Forwarded-For, which Nginx sets from the real client IP.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=[])
