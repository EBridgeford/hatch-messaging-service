from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    twilio_api_key: str
    sendgrid_api_key: str
    fastapi_debug: bool

    class Config:
        env_file = ".env"


settings = Settings()
