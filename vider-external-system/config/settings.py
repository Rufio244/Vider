from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # การเชื่อมต่อ
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    AUTO_RECONNECT: bool = True
    RECONNECT_DELAY: int = 5  # วินาที

    # ความปลอดภัย
    ENCRYPTION_KEY: str = "GENERATE_YOUR_OWN_SECURE_KEY_HERE"
    ACCESS_KEY: str = "YOUR_SECRET_ACCESS_KEY_FOR_VIDER"
    TOKEN_EXPIRE_MINUTES: int = 5

    # ฐานข้อมูล
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost/vider_external_db"

settings = Settings()

