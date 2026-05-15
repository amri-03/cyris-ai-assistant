from pydantic import BaseModel
from datetime import datetime, UTC


class RuntimeAdaptationRecord(BaseModel):
    runtime_health: str

    throttle_mode: str

    runtime_priority: str

    timestamp: datetime = (
        datetime.now(UTC)
    )