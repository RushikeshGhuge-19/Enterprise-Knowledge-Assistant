from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    uploaded_by: int
    created_at: datetime

    class Config:
        from_attributes = True