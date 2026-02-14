from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GCSState(BaseModel):
    test_mode: Optional[bool] = False
    timestamp_ms: Optional[int] = None
    timestamp: Optional[datetime] = None
