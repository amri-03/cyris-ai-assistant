from pydantic import BaseModel


class SystemState(BaseModel):
    continuity_score: int = 0

    overload_detected: bool = False

    fragmentation_level: str = "low"

    inactivity_days: int = 0

    current_focus_state: str = "maintenance"

    escalation_level: str = "low"