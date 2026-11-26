"""Expose basic information about the running API."""

from fastapi import APIRouter , Depends

import os  
from helpers.config import get_settings , Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)


@base_router.get("/")
async  def welcome(app_settings: Settings = Depends(get_settings)):
    """Return a welcome message and app version from the injected settings."""
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    author = app_settings.AUTHOR

    return {
        "message": f"Welcome to the {app_name}! made by {author}",
        "version": app_version
    }
