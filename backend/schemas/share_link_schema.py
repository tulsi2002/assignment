from pydantic import BaseModel, Field
from datetime import datetime

class ShareLinkCreate(BaseModel):
    expiry_minutes : int 
    one_time : bool = False

class ShareLinkOut(BaseModel):
    public_link : str
    expiry_time : datetime
    one_time : bool
    accessed : bool