from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./database/finance_tracker.db"
    
    # Këto duhet të jenë si fusha për të mos dhënë error
    alpha_vantage_key: str = ""
    news_api_key: str = ""
    openweather_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()