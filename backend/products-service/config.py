from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Products service"
    DOCS_URL: str = '/api/products/docs'
    OPENAPI_URL: str = '/api/products/openapi.json'
    DEBUG_MODE: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8002
    DB_URL: str
    DB_NAME: str
    JWT_SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
