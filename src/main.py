from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient

from helpers.config import get_settings
from routes import base, data


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    mongo_conn = AsyncMongoClient(settings.MONGO_URI)
    try:
        app.mongo_conn = mongo_conn
        app.db_client = mongo_conn[settings.MONGO_DATABASE]
        yield
    finally:
        await mongo_conn.close()


app = FastAPI(lifespan=lifespan)
app.include_router(base.base_router)
app.include_router(data.data_router)
