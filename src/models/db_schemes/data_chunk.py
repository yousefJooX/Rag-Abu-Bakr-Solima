"""Define the fields used to represent a stored text chunk."""

from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    """Describe a chunk's text, source metadata, position, and owning project.

    The positive chunk_order records the chunk's position. The chunk_project_id
    links it to the project's MongoDB _id.
    """

    id: Optional[ObjectId] = Field(None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId

    class Config:
        """Allow MongoDB ObjectId values in this Pydantic schema."""

        arbitrary_types_allowed = True
