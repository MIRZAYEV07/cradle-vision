from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class RtspUrlBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# Properties to receive on item creation
class RtspUrlCreate(RtspUrlBase):
    id: int
    rtsp_url: str


# Properties to receive on item update
class RtspUrlUpdate(RtspUrlBase):
    pass


# Properties shared by models stored in DB
class RtspUrlInDBBase(RtspUrlBase):
    id: int
    rtsp_url: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class RtspUrl(RtspUrlInDBBase):
    pass


# Properties properties stored in DB
class RtspUrlInDB(RtspUrlInDBBase):
    pass

