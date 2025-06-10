from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# output schema
class DocumentOut(BaseModel):
    id : int
    file_name : str
    file_type : str
    file_size : int
    owner_id : int
    created_at : datetime
    