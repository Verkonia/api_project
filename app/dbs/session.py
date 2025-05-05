""""Модуль для создания сессий базы данных с помощью SQLModel"""

from sqlmodel import Session
from app.dbs.database import engine

def get_session():
    """Создает сессию базы данных"""
    with Session(engine) as session:
        yield session
