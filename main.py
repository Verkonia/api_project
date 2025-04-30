from fastapi import FastAPI
from dbs.database import init_db
from routes import user, movie


app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(user.router)
app.include_router(movie.router)