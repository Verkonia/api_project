from fastapi import FastAPI
from app.dbs.database import init_db
from app.routes import user, movie


app = FastAPI()

@app.get("/")
async def root():
    return {"status": "OK"}

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(user.router)
app.include_router(movie.router)