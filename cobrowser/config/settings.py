from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings and configuration
    """
    APP_NAME: str = "CoBrowser"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./cobrowser.db"
    
    # Redis settings for Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env" 