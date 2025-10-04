from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field("HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60 * 24 * 7, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    mongodb_url: str = Field("mongodb://localhost:27017", alias="MONGODB_URL")
    mongodb_db: str = Field("mental_wellness", alias="MONGODB_DB")
    redis_url: str = Field("redis://localhost:6379/0", alias="REDIS_URL")
    fernet_key: str = Field(..., alias="FERNET_KEY")
    
    # Groq API Configuration
    groq_api_key: str = Field(..., alias="GROQ_API_KEY")
    groq_model: str = Field("mixtral-8x7b-32768", alias="GROQ_MODEL")

    # ✅ v2 style config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,    # allow using field names
        case_sensitive=False      # allow uppercase in .env
    )

settings = Settings()
