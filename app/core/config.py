from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    phone_verify_api_key: str
    db_username: str
    db_password: str
    db_hostname: str
    db_port: int
    db_name: str
    secret_key: str
    algorithm: str
    expiray: int
    client_id: str
    client_secret: str
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str


settings = Settings()
