class ReflectionService:

    def evaluate_guidance_effectiveness(
            self,
            recommendation_followed: bool,
            continuity_change: int,
            overload_detected: bool
    ):

        if (
                recommendation_followed
                and continuity_change > 0
        ):
            return {
                "reflection_result": "positive_adaptation",
                "adjustment": (
                    "Current guidance style appears effective."
                )
            }

        if overload_detected:
            return {
                "reflection_result": "pressure_too_high",
                "adjustment": (
                    "Guidance intensity should be reduced to avoid overload escalation."
                )
            }

        return {
            "reflection_result": "neutral",
            "adjustment": (
                "Continue observing behavioral response patterns."
            )
        }