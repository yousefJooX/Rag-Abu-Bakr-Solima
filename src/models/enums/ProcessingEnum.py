"""List the file extensions supported by the processing pipeline."""

from enum import Enum

class ProcessingEnum(Enum):
    """Match supported extensions to the text and PDF loader branches."""

    TXT = ".txt"
    PDF = ".pdf"
