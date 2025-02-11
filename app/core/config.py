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

    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    spreadsheet_title: str = 'Топ проектов по скорости закрытия на {} по UTC'
    spreadsheet_header: list = ['Название проекта', 'Дней сбора', 'Описание']
    spreadsheet_title_header_row_quantity: int = 2
    spreadsheet_column_quantity: int = 3

    class Config:
        """Конфигурация настроек приложения."""

        env_file = '.env'


settings = Settings()
