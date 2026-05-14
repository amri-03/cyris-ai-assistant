from pydantic import BaseModel
from typing import List


class StateHistory(BaseModel):
    behavior_events: List[str] = []

    context_changes: List[str] = []

    priority_changes: List[str] = []