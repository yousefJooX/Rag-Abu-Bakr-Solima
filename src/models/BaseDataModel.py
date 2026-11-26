"""Supply the common dependencies used by MongoDB models."""

from helpers.config import get_settings


class BaseDataModel:
    """Keep the database handle and app settings available to each model."""

    def __init__(self, db_client: object):
        """Store the supplied database handle and load the application's settings."""
        self.db_client = db_client
        self.app_settings = get_settings()
