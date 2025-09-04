from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "DEFAULT"
    POSTGRES_USER: str = "DEFAULT"
    POSTGRES_PASSWORD: str = "DEFAULT"
    POSTGRES_DB: str = "DEFAULT"
    POSTGRES_HOST: str = "DEFAULT"
    POSTGRES_PORT: int = 5432
    SECRET_KEY: str = "DEFAULT"
    ALGORITHM: str = "DEFAULT"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}"
            f":{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = "../.dev.env"
        env_file_encoding = "utf-8"

settings = Settings()

