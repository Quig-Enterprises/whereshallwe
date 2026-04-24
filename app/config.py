from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = False
    APP_ENV: str = "production"
    MAPBOX_TOKEN: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

if settings.APP_ENV == "production" and settings.DEBUG:
    raise RuntimeError("DEBUG=true is prohibited when APP_ENV=production")
if len(settings.SECRET_KEY) < 32 or settings.SECRET_KEY in ("CHANGE_ME", "changeme", "secret"):
    raise RuntimeError("SECRET_KEY must be at least 32 characters and not a placeholder")
