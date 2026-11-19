from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BeeAiry API"
    database_url: str = "sqlite:///./beeairy.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
