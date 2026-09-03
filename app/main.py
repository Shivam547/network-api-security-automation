from fastapi import FastAPI

from app.database import Base, engine
from app import models

from app.routers import auth
from app.routers import users


app = FastAPI(
    title="Enterprise Security Test API",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(users.router)


@app.get("/health")
def health_check():

    return {
        "status": "UP"
    }