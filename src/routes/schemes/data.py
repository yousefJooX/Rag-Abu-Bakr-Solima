"""Define the JSON body accepted by the file-processing endpoint."""

from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    """Identify the saved file and set the chunk size and overlap in characters."""

    file_id: str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    # Use 1 to clear the project's existing chunks before storing this file's chunks.
    do_reset: Optional[int] = 0
