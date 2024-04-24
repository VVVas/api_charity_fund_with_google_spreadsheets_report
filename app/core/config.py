from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = 'QRKot'
    app_description: str = 'Пожертвования на проекты'

    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'

    secret: str = 'SECRET'
    authentication_strategy_lifetime_seconds: int = 3600
    min_password_len: int = 3

    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        """Конфигурация настроек приложения."""

        env_file = '.env'


settings = Settings()