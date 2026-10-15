from fastapi import APIRouter , Depends

import os  
from helpers.config import get_settings , Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)


@base_router.get("/")
async  def welcome(app_settings: Settings = Depends(get_settings)): #  make it  more efficient by using Depends to inject the settings dependency into the route handler

    #app_settings = get_settings()

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    author = app_settings.AUTHOR

    return {
        "message": f"Welcome to the {app_name}! made by {author}",
        "version": app_version
    }