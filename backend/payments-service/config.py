from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Payments service"
    DOCS_URL: str = '/api/payments/docs'
    OPENAPI_URL: str = '/api/payments/openapi.json'
    DEBUG_MODE: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8004
    DB_URL: str
    DB_NAME: str
    JWT_SECRET_KEY: str
    NATS_URL: str
    NATS_CLUSTER_ID: str
    STRIPE_SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
