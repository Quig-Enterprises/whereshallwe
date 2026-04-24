-- Migration 001: public.domains table
CREATE TABLE IF NOT EXISTS public.domains (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hostname    TEXT UNIQUE NOT NULL,
    site        TEXT NOT NULL CHECK (site IN ('wswd', 'wsws')),
    theme_name  TEXT NOT NULL,
    site_name   TEXT NOT NULL,
    is_active   BOOLEAN NOT NULL DEFAULT true,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO public.domains (hostname, site, theme_name, site_name)
VALUES
    ('whereshallwedance.com', 'wswd', 'wswd', 'Where Shall We Dance'),
    ('whereshallweski.com',   'wsws', 'wsws', 'Where Shall We Ski')
ON CONFLICT (hostname) DO NOTHING;
