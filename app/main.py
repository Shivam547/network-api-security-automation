from fastapi import FastAPI

from app.database import Base, engine
from app import models

from app.routers import auth
from app.routers import users
from app.routers import orders
from app.routers import rate_limit
from app.seed import seed_users


app = FastAPI(
    title="Enterprise Security Test API",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)
seed_users()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(rate_limit.router)


@app.get("/health")
def health_check():

    return {
        "status": "UP"
    }