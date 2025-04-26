from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv(".env", override=True)

class Settings(BaseSettings):

    GOOGLE_API_KEY: str
    GOOGLE_GENERATIVE_MODEL: str
    MAX_TOKENS: int
    TEMPERATURE: float

    class Config:
        env_file = ".env"
        override = True
        str_strip_whitespace = True
        validate_assignment = True

@lru_cache()
def get_settings():
    return Settings()


