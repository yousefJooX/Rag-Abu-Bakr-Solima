"""Define and validate the fields stored for a project."""

from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    """Represent a MongoDB project document.

    The project_id comes from the app. The optional id maps to MongoDB's _id
    and can be filled in after the document is inserted.
    """

    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @validator('project_id')
    def validate_project_id(cls, value):
        """Reject project IDs that contain characters other than letters and numbers."""
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        
        return value

    class Config:
        """Allow the schema to hold a MongoDB ObjectId as a Python value."""

        arbitrary_types_allowed = True
