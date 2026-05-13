from pydantic import BaseModel
from typing import List, Optional


class UserProfile(BaseModel):
    name: str

    long_term_goals: List[str] = []
    active_focus_areas: List[str] = []
    recurring_interests: List[str] = []

    current_challenges: List[str] = []
    distractions: List[str] = []

    preferred_work_style: Optional[str] = None

    productivity_hours: List[str] = []