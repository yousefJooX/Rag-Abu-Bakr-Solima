"""Create the FastAPI app and register its routes."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient

from helpers.config import get_settings
from routes import base, data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Make MongoDB available while the app runs and close the client on shutdown.

    Store the client and selected database on the app before it starts serving
    requests so database operations can share the same client.
    """
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
