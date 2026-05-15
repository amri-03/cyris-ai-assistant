class RuntimeThrottleService:

    def evaluate_throttle(
            self,
            runtime_health: str
    ):

        if runtime_health == "stressed":
            return {
                "throttle_mode": "reduced_execution",
                "guidance": (
                    "Reduce orchestration intensity temporarily."
                )
            }

        if runtime_health == "active":
            return {
                "throttle_mode": "balanced_execution",
                "guidance": (
                    "Maintain manageable runtime orchestration."
                )
            }

        return {
            "throttle_mode": "normal_execution",
            "guidance": (
                "Runtime orchestration operating normally."
            )
        }