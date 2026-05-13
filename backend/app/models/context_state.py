from pydantic import BaseModel
from typing import Optional


class ContextState(BaseModel):
    current_mode: Optional[str] = None

    available_time: Optional[str] = None

    energy_level: Optional[str] = None

    workload_level: Optional[str] = None

    current_priority: Optional[str] = None