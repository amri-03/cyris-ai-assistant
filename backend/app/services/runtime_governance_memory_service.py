from app.models.runtime_governance_record import (
    RuntimeGovernanceRecord
)


class RuntimeGovernanceMemoryService:

    def __init__(self):
        self.governance_history = []

    def record_governance(
            self,
            governance_mode: str,
            equilibrium_state: str,
            runtime_prediction: str
    ):
        governance = (
            RuntimeGovernanceRecord(
                governance_mode=governance_mode,
                equilibrium_state=equilibrium_state,
                runtime_prediction=runtime_prediction
            )
        )

        self.governance_history.append(
            governance
        )

    def get_governance_history(self):
        return self.governance_history