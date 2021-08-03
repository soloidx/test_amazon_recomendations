from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Amazon reviews service"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///app.db"


settings = Settings()
