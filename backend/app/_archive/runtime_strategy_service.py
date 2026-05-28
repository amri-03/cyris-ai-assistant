class RuntimeStrategyService:

    def evaluate_strategy_effectiveness(
            self,
            adaptation_history: list
    ):

        if len(adaptation_history) < 3:
            return {
                "strategy_state": "insufficient_runtime_data"
            }

        latest = adaptation_history[-1]

        if (
                latest.runtime_health == "stable"
                and latest.throttle_mode == "normal_execution"
        ):
            return {
                "strategy_state": "effective",
                "guidance": (
                    "Current runtime orchestration strategy appears stable."
                )
            }

        if latest.runtime_health == "stressed":
            return {
                "strategy_state": "overloaded",
                "guidance": (
                    "Current runtime orchestration may require stabilization adjustments."
                )
            }

        return {
            "strategy_state": "adaptive_monitoring",
            "guidance": (
                "Runtime orchestration strategy is still evolving."
            )
        }