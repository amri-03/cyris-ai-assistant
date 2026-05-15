class RuntimeHealthService:

    def evaluate_runtime_health(
            self,
            total_runtime_cycles: int,
            overload_detected: bool
    ):

        if (
                total_runtime_cycles >= 10
                and overload_detected
        ):
            return {
                "runtime_health": "stressed",
                "guidance": (
                    "Runtime orchestration pressure appears elevated."
                )
            }

        if total_runtime_cycles >= 5:
            return {
                "runtime_health": "active",
                "guidance": (
                    "Runtime orchestration is operating continuously."
                )
            }

        return {
            "runtime_health": "stable",
            "guidance": (
                "Runtime orchestration appears stable."
            )
        }