from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str
    GROQ_API_KEY: str
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instancia global para importar en cualquier módulo
settings = Settings()