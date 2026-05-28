class RuntimeReflectionService:

    def reflect_on_runtime_behavior(
            self,
            adaptation_history: list
    ):

        if len(adaptation_history) < 5:
            return {
                "reflection_state": (
                    "insufficient_reflection_data"
                )
            }

        stable_count = sum(
            1
            for item in adaptation_history
            if item.runtime_health == "stable"
        )

        stressed_count = sum(
            1
            for item in adaptation_history
            if item.runtime_health == "stressed"
        )

        if stable_count > stressed_count:
            return {
                "reflection_state": (
                    "runtime_behavior_improving"
                ),
                "guidance": (
                    "Adaptive orchestration appears increasingly stable."
                )
            }

        return {
            "reflection_state": (
                "runtime_behavior_requires_refinement"
            ),
            "guidance": (
                "Runtime adaptation strategies may require improvement."
            )
        }