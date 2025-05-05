"""Создаёт приложение FastAPI и подключает к нему маршруты и базу данных"""

from fastapi import FastAPI
from app.dbs.database import init_db
from app.routes import user, movie


app = FastAPI()

@app.get("/")
async def root():
    """возвращает статус приложения"""
    return {"status": "OK"}

@app.on_event("startup")
def on_startup():
    """инициализирует базу данных при запуске приложения"""
    init_db()

app.include_router(user.router)
app.include_router(movie.router)
