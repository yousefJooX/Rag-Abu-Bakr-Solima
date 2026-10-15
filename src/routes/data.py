from fastapi import APIRouter , Depends , UploadFile
import os  
from helpers.config import get_settings , Settings


data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str,file: UploadFile, 
                      app_settings: Settings = Depends(get_settings)):
    # validate file extension &  size   we can do the logic here but abobaker have another apporoch 
    # and do it inside the controller  make all  logic for the data
    pass  # TODO: call DataController().validate_uploaded_file(file)
