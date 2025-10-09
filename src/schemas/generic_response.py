from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any


class GenericResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: str
    timestamp: datetime


