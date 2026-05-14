from pydantic import BaseModel
from typing import List


class SessionState(BaseModel):
    recent_focus_areas: List[str] = []

    recent_recommendations: List[str] = []

    continuity_score: int = 0

    last_known_status: str = "unknown"