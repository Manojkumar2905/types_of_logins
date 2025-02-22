from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FIRSTOCK_MONGODB_CREDENTIALS: str
    CLIENT_DB: str
    CLIENT_DETAILS: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
