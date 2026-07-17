from fastapi import FastAPI

from . import models
from .database import engine
from .routers import Posts, Users


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


app.include_router(Posts.router)
app.include_router(Users.router)