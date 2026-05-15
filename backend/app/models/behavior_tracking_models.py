from pydantic import BaseModel
from datetime import datetime, UTC
from typing import Optional


class BehaviorSignal(BaseModel):
    signal_type: str

    recorded_at: datetime = (
        datetime.now(UTC)
    )

    metadata: Optional[dict] = None


class ContinuityRecord(BaseModel):
    interaction_count: int = 0

    last_interaction_at: datetime = (
        datetime.now(UTC)
    )

    continuity_state: str = (
        "active"
    )


class FocusPattern(BaseModel):
    active_focus: Optional[str] = None

    focus_switch_count: int = 0

    last_updated: datetime = (
        datetime.now(UTC)
    )