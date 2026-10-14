from fastapi import APIRouter
import os  

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)


@base_router.get("/")
async  def welcome():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    author = os.getenv("AUTHOR")

    return {
        "message": f"Welcome to the {app_name}! made by {author}",
        "version": app_version
    }