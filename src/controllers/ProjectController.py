"""Manage the local storage folder for each project."""

import os

from .BaseController import BaseController


class ProjectController(BaseController):
    """Keep uploaded files in a separate folder for each project ID."""

    def __init__(self):
        """Initialize the shared settings and upload directory from BaseController."""
        super().__init__()

    def get_project_path(self, project_id: str):
        """Return the project's upload directory, creating it on the first use."""
        project_dir = os.path.join(
            self.files_dir,
            project_id
        )

        os.makedirs(project_dir, exist_ok=True)

        return project_dir
