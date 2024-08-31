from decouple import config as env_config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = 'Graintrack'
    PROJECT_VERSION: str = '0.0.1'

    # API version prefixes
    API_V1_PREFIX: str = '/api/v1'

    # Resource prefixes
    AUTH_API_PREFIX: str = '/auth'
    CATEGORY_API_PREFIX: str = '/category'
    PRODUCT_API_PREFIX: str = '/product'

    # DB credentials
    DB_NAME: str = env_config('DB_NAME')
    DB_USER: str = env_config('DB_USER')
    DB_PASSWORD: str = env_config('DB_PASSWORD')
    DB_HOST: str = env_config('DB_HOST')
    DB_PORT: str = env_config('DB_PORT')
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{env_config('DB_NAME')}"
    )

    # Security
    ACCESS_TOKEN_SECRET: str = env_config('ACCESS_TOKEN_SECRET')
    REFRESH_TOKEN_SECRET: str = env_config('REFRESH_TOKEN_SECRET')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = env_config('ACCESS_TOKEN_EXPIRE_MINUTES')
    REFRESH_TOKEN_EXPIRE_HOURS: int = env_config('REFRESH_TOKEN_EXPIRE_HOURS')
    JWT_ALGORITHM: str = env_config('JWT_ALGORITHM')


settings = Settings()
