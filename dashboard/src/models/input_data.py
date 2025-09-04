from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class TelemetryInput(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
