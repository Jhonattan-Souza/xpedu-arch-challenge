from fastapi import FastAPI
from app.routers import customers
from app.infrastructure.session import Base, engine

app = FastAPI()

app.include_router(customers.router)

Base.metadata.create_all(bind=engine)