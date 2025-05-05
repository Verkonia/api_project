"""Модуль для инициализации базы данных и подключения к SQLite"""

from sqlmodel import create_engine, SQLModel

engine = create_engine('sqlite:///./library.db',echo=True)

def init_db():
    """Создание таблиц в базе данных"""
    SQLModel.metadata.create_all(engine)
