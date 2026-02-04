
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class DownloadRequest(BaseModel):
    urls: List[str]

class DownloadResponse(BaseModel):
    job_id: Optional[str] = None
    results: Optional[List[dict]] = None
    message: str

class MediaInfo(BaseModel):
    media_url: str
    media_type: str
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    filename: str

class ErrorResponse(BaseModel):
    detail: str
