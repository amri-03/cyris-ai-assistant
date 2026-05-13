from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BehaviorEvent(BaseModel):
    event_type: str

    focus_area: Optional[str] = None

    engagement_level: Optional[int] = None

    notes: Optional[str] = None

    timestamp: datetime = datetime.now()