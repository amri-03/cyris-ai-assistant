class RuntimeEquilibriumService:

    def evaluate_runtime_equilibrium(
            self,
            adaptation_history: list
    ):
        protective_count = sum(
            1
            for item in adaptation_history
            if (
                    item.runtime_priority
                    == "critical_recovery"
            )
        )

        normal_count = sum(
            1
            for item in adaptation_history
            if (
                    item.runtime_priority
                    == "normal_operation"
            )
        )

        if protective_count > normal_count * 2:
            return {
                "equilibrium_state": (
                    "overprotective_runtime_behavior"
                ),
                "guidance": (
                    "Runtime orchestration may be excessively defensive."
                )
            }

        return {
            "equilibrium_state": (
                "balanced_runtime_behavior"
            ),
            "guidance": (
                "Runtime orchestration appears operationally balanced."
            )
        }