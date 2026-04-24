-- Migration 003: wsws schema (ski resorts)
CREATE SCHEMA IF NOT EXISTS wsws;

CREATE TABLE IF NOT EXISTS wsws.venues (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug                  TEXT UNIQUE NOT NULL,
    name                  TEXT NOT NULL,
    address               TEXT,
    city                  TEXT,
    state                 TEXT,
    zip                   TEXT,
    lat                   NUMERIC(10, 7),
    lng                   NUMERIC(10, 7),
    website               TEXT,
    phone                 TEXT,
    email                 TEXT,
    description           TEXT,
    categories            TEXT[],
    is_featured           BOOLEAN NOT NULL DEFAULT false,
    status                TEXT NOT NULL DEFAULT 'active',
    primary_photo         TEXT,
    avg_rating            NUMERIC(3, 2),
    rating_count          INT NOT NULL DEFAULT 0,
    -- ski-specific
    trail_count           INT,
    lift_count            INT,
    vertical_drop_ft      INT,
    summit_elevation_ft   INT,
    base_elevation_ft     INT,
    season_opens          DATE,
    season_closes         DATE,
    snow_depth_in         INT,
    conditions_updated_at TIMESTAMPTZ,
    terrain_url           TEXT,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_wsws_venues_state ON wsws.venues (state);
CREATE INDEX IF NOT EXISTS idx_wsws_venues_status ON wsws.venues (status);

CREATE TABLE IF NOT EXISTS wsws.venue_photos (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    venue_id      UUID NOT NULL REFERENCES wsws.venues(id) ON DELETE CASCADE,
    url           TEXT NOT NULL,
    display_order INT NOT NULL DEFAULT 0,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS wsws.venue_conditions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    venue_id        UUID NOT NULL REFERENCES wsws.venues(id) ON DELETE CASCADE,
    reported_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    snow_depth_in   INT,
    open_trails     INT,
    open_lifts      INT,
    conditions_text TEXT
);

CREATE INDEX IF NOT EXISTS idx_wsws_conditions_venue_time ON wsws.venue_conditions (venue_id, reported_at DESC);
