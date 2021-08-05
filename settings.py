from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Amazon reviews service"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///app.db"
    RAINFOREST_API_URL: str
    RAINFOREST_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
