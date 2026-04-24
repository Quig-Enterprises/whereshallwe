-- Migration 002: wswd schema (dance venues)
CREATE SCHEMA IF NOT EXISTS wswd;

CREATE TABLE IF NOT EXISTS wswd.venues (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug            TEXT UNIQUE NOT NULL,
    name            TEXT NOT NULL,
    address         TEXT,
    city            TEXT,
    state           TEXT,
    zip             TEXT,
    lat             NUMERIC(10, 7),
    lng             NUMERIC(10, 7),
    website         TEXT,
    phone           TEXT,
    email           TEXT,
    facebook_url    TEXT,
    twitter_handle  TEXT,
    description     TEXT,
    categories      TEXT[],
    is_featured     BOOLEAN NOT NULL DEFAULT false,
    status          TEXT NOT NULL DEFAULT 'active',
    primary_photo   TEXT,
    avg_rating      NUMERIC(3, 2),
    rating_count    INT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_wswd_venues_categories ON wswd.venues USING GIN (categories);
CREATE INDEX IF NOT EXISTS idx_wswd_venues_city_state ON wswd.venues (city, state);
CREATE INDEX IF NOT EXISTS idx_wswd_venues_status ON wswd.venues (status);

CREATE TABLE IF NOT EXISTS wswd.venue_photos (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    venue_id      UUID NOT NULL REFERENCES wswd.venues(id) ON DELETE CASCADE,
    url           TEXT NOT NULL,
    display_order INT NOT NULL DEFAULT 0,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
