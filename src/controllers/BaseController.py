"""Provide shared settings and file storage helpers for controllers."""

import os
from helpers.config import Settings , get_settings
import  random , string
class BaseController:
    """Give controllers a common location for uploaded files."""

    def __init__(self):
        """Load settings and resolve the storage path relative to the source folder."""
        self.app_settings: Settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.base_dir, "assets", "files")       
    def generate_random_string(self, length: int = 12 ) -> str:
        """Generate a prefix of letters and digits for a stored filename."""
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length))
