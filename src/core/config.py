from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        server = self.POSTGRES_SERVER
        port = self.POSTGRES_PORT
        db_name = self.POSTGRES_DB

        return f"postgresql://{user}:{password}@{server}:{port}/{db_name}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
