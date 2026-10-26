from fastapi import FastAPI
from helpers.config import get_settings
from routes import base ,data
from pymongo import AsyncMongoClient
app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()

app.include_router(base.base_router)
app.include_router(data.data_router)