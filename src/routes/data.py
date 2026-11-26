"""Expose endpoints to upload and process a project's files."""

import logging
from typing import Annotated

import aiofiles
from fastapi import APIRouter, Depends, Request, UploadFile, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from controllers import DataController, ProcessController
from helpers.config import Settings, get_settings
from models import ResponseSignal
from models.ProjectModel import ProjectModel

from .schemes.data import ProcessRequest

logger = logging.getLogger('uvicorn.error')
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)


@data_router.post("/upload/{project_id}")
async def upload_data(
    request: Request,
    project_id: str,
    file: UploadFile,
    app_settings: Annotated[Settings, Depends(get_settings)],
):
    """Save a file under its project and return the identifiers needed for processing."""
    data_controller = DataController()

    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal}
        )

    project_model = ProjectModel(db_client=request.app.db_client)
    try:
        project = await project_model.get_project_or_create_one(project_id)
    except ValidationError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROJECT_ID_INVALID.value},
        )

    try:
        file_path, file_id = data_controller.generate_unique_filepath(
            orig_file_name=file.filename,
            project_id=project.project_id,
        )
        # Copy the upload in blocks so memory use stays bounded while writing.
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:

        logger.error(f"Error while uploading file: {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
            "file_id": file_id,
            "project_id": project.project_id,
            "mongo_project_id": str(project.id),
        }
    )


@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, request: ProcessRequest):
    """Load a saved file, split its text, and return the chunks and metadata."""
    file_id = request.file_id
    chunk_size = request.chunk_size
    overlap_size = request.overlap_size
    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)
    if file_content is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_PROCESSING_FAILED.value}
        )
    chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )
    if chunks is None or len(chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_PROCESSING_FAILED.value}
        )
    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_PROCESSED_SUCCESSFULLY.value,
            "file_id": file_id,
            "num_chunks": len(chunks),
            "chunks": [c.model_dump() for c in chunks],
        }
    )
