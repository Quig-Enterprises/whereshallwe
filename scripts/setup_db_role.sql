-- Run once as postgres superuser before migrations.
-- Generates a random password for whereshallwe_app role.
-- After running, record the password in /var/www/html/whereshallwe/.env

-- Create the application role (will error if already exists — safe to rerun with IF NOT EXISTS in pg13+)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'whereshallwe_app') THEN
        CREATE ROLE whereshallwe_app LOGIN PASSWORD 'PLACEHOLDER_REPLACE_ME';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE whereshallwe TO whereshallwe_app;
GRANT USAGE ON SCHEMA public TO whereshallwe_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO whereshallwe_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO whereshallwe_app;

-- Grant after schemas are created (run after migration 002 + 003):
-- GRANT USAGE ON SCHEMA wswd, wsws TO whereshallwe_app;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA wswd TO whereshallwe_app;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA wsws TO whereshallwe_app;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA wswd GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO whereshallwe_app;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA wsws GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO whereshallwe_app;
