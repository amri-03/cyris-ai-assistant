from pydantic import BaseModel
from typing import Optional


class UserLifecycle(BaseModel):
    current_stage: str

    consistency_level: Optional[str] = None

    engagement_status: Optional[str] = None

    dominant_focus_area: Optional[str] = None

    burnout_risk: Optional[str] = None

    last_active_days_ago: Optional[int] = None