from pydantic import BaseModel
from typing import List


class PriorityState(BaseModel):
    high_priority: List[str] = []

    medium_priority: List[str] = []

    low_priority: List[str] = []