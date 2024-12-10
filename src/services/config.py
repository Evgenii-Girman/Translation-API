from pydantic import BaseSettings

class Settings(BaseSettings):
    MODEL_DIR: str = "../models_storage"
    PRECACHE_MODELS: str = "en-de,de-en,en-fr,fr-en"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
