"""Validate uploads and choose where to store them on disk."""

from models import ResponseSignal
from .ProjectController import ProjectController    
from  .BaseController import BaseController
from fastapi import UploadFile
import  re
import os
class DataController(BaseController):
    """Apply upload limits and give each accepted file a storage path."""

    def __init__(self):
        """Load shared settings and set the conversion factor for file sizes."""
        super().__init__()
        self.size_scale = 1024 * 1024

    def validate_uploaded_file(self, file: UploadFile):
        """Check the upload's declared content type and size against the settings.

        Return a boolean and a message the route can use in its response.
        """
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_ALLOWED.value

        if file.size > self.app_settings.FILE_MAX_SIZE_MB * self.size_scale: 
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value.format(
                max_size=self.app_settings.FILE_MAX_SIZE_MB
            )
        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value

    def generate_unique_filepath(self, orig_file_name: str, project_id: str):
        """Return an unused path in the project's folder and its filename as the file ID.

        Prefix the cleaned name with a random key so uploads with the same
        original filename can be stored separately.
        """
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_file_name = self.get_clean_file_name(
            orig_file_name=orig_file_name
        )

        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path, random_key + "_" + cleaned_file_name

    def get_clean_file_name(self, orig_file_name: str):
        """Keep letters, numbers, underscores, and dots from the original filename."""
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
