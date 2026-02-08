from pydantic import BaseModel
from typing import Optional

class GCSState(BaseModel):
    gcs_test_mode: Optional[bool] = False
