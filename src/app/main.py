from fastapi import FastAPI

from app.routers.contact import router

app = FastAPI(title="Testcontainers Practice")
app.include_router(router)