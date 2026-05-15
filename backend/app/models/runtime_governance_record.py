from pydantic import BaseModel
from datetime import datetime, UTC


class RuntimeGovernanceRecord(BaseModel):
    governance_mode: str

    equilibrium_state: str

    runtime_prediction: str

    timestamp: datetime = (
        datetime.now(UTC)
    )