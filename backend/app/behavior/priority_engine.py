from app.models.priority_state import PriorityState


class PriorityEngine:

    def adjust_priorities(
            self,
            priorities: PriorityState,
            behavior_signal: str,
            context_mode: str
    ) -> dict:

        updated_priorities = {
            "high_priority": priorities.high_priority,
            "medium_priority": priorities.medium_priority,
            "low_priority": priorities.low_priority
        }

        if behavior_signal == "reduce_complexity":
            return {
                "status": "adjusted",
                "strategy": (
                    "Priority complexity reduced "
                    "due to behavioral overload signals."
                ),
                "updated_priorities": updated_priorities
            }

        if context_mode == "reduced_pressure":
            return {
                "status": "adjusted",
                "strategy": (
                    "Reduced-pressure mode activated "
                    "due to workload conditions."
                ),
                "updated_priorities": updated_priorities
            }

        return {
            "status": "stable",
            "strategy": (
                "Current priorities remain stable."
            ),
            "updated_priorities": updated_priorities
        }