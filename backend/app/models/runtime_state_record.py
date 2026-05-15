from pydantic import BaseModel
from datetime import datetime, UTC


class RuntimeStateRecord(BaseModel):
    focus_state: str

    continuity_score: int

    overload_detected: bool

    timestamp: datetime