from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Orders service"
    DOCS_URL: str = '/api/orders/docs'
    OPENAPI_URL: str = '/api/orders/openapi.json'
    DEBUG_MODE: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8003
    DB_URL: str
    DB_NAME: str
    JWT_SECRET_KEY: str
    NATS_URL: str
    NATS_CLUSTER_ID: str

    class Config:
        env_file = ".env"


settings = Settings()
