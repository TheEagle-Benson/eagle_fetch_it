from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  APP_NAME: str = "Eagle Fetch It"
  DEBUG: bool = True
  HOST: str = "127.0.0.1"
  PORT: int = 5000

  model_config = SettingsConfigDict(env_file=".env")

settings = Settings()