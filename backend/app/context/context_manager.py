from app.models.context_state import ContextState


class ContextManager:

    def evaluate_context(
            self,
            context: ContextState
    ) -> dict:

        if context.workload_level == "high":
            return {
                "mode": "reduced_pressure",
                "recommendation": (
                    "Current workload appears high. "
                    "Focus on smaller achievable progress."
                )
            }

        if context.energy_level == "low":
            return {
                "mode": "light_focus",
                "recommendation": (
                    "Energy levels appear low. "
                    "Avoid heavy cognitive workload right now."
                )
            }

        if context.available_time == "high":
            return {
                "mode": "deep_work",
                "recommendation": (
                    "A larger focus session may be suitable right now."
                )
            }

        return {
            "mode": "balanced",
            "recommendation": (
                "Maintain steady progress with manageable tasks."
            )
        }