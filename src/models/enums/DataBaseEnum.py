"""Define the names used to select MongoDB collections."""

from enum import Enum


class DataBaseEnum(Enum):
    """Keep collection names consistent wherever database models select them."""

    COLLECTION_PROJECT_NAME = "projects"
    COLLECTION_CHUNK_NAME = "chunks"
    COLLECTION_ASSET_NAME = "assets"
