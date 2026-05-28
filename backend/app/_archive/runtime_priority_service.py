class RuntimePriorityService:

    def evaluate_runtime_priority(
            self,
            runtime_health: str,
            escalation_level: str
    ):

        if (
                runtime_health == "stressed"
                and escalation_level == "high"
        ):
            return {
                "runtime_priority": "critical_recovery",
                "guidance": (
                    "Prioritize stabilization and continuity recovery systems."
                )
            }

        if escalation_level == "moderate":
            return {
                "runtime_priority": "balanced_support",
                "guidance": (
                    "Maintain adaptive support and continuity monitoring."
                )
            }

        return {
            "runtime_priority": "normal_operation",
            "guidance": (
                "Runtime orchestration operating under normal conditions."
            )
        }