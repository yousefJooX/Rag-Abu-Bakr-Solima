"""Define the JSON body accepted by the file-processing endpoint."""

from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    """Identify the saved file and set the chunk size and overlap in characters."""

    file_id: str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    # The schema accepts this flag, but the route does not read it yet.
    do_reset : Optional[int] = 0
