from app.services.runtime_governance_memory_service import (
    RuntimeGovernanceMemoryService
)


class RuntimeGovernanceService:

    def __init__(self):

        self.governance_memory = (
            RuntimeGovernanceMemoryService()
        )

    def evaluate_runtime_governance(
            self,
            equilibrium_state: str,
            runtime_prediction: str
    ):

        if (
                equilibrium_state
                == "overprotective_runtime_behavior"
        ):

            governance = {
                "governance_mode": (
                    "runtime_rebalancing"
                ),
                "guidance": (
                    "Reduce excessive protective orchestration behavior."
                )
            }

        elif (
                runtime_prediction
                == "high_runtime_instability_risk"
        ):

            governance = {
                "governance_mode": (
                    "protective_runtime_control"
                ),
                "guidance": (
                    "Increase runtime stabilization governance."
                )
            }

        else:

            governance = {
                "governance_mode": (
                    "stable_runtime_governance"
                ),
                "guidance": (
                    "Runtime orchestration governance remains stable."
                )
            }

        self.governance_memory.record_governance(
            governance_mode=(
                governance["governance_mode"]
            ),
            equilibrium_state=equilibrium_state,
            runtime_prediction=runtime_prediction
        )

        return governance