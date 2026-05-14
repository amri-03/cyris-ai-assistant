from pydantic import BaseModel
from typing import List


class ClassifiedMemory(BaseModel):
    persistent_identity: List[str] = []

    temporary_context: List[str] = []

    behavioral_patterns: List[str] = []

    adaptive_priorities: List[str] = []