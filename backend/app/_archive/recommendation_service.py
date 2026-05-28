class RecommendationService:

    def generate_recommendation(
            self,
            focus_area: str,
            energy_level: str,
            available_time: str
    ):

        if (
                energy_level == "low"
                and available_time == "short"
        ):
            return {
                "recommendation_type": "light_progress",
                "action": (
                    f"Spend 20 minutes making lightweight progress in "
                    f"{focus_area}."
                ),
                "reasoning": (
                    "Current conditions favor low-resistance progress."
                )
            }

        if available_time == "high":
            return {
                "recommendation_type": "deep_work",
                "action": (
                    f"Schedule a focused deep-work session for "
                    f"{focus_area}."
                ),
                "reasoning": (
                    "Current conditions support higher cognitive investment."
                )
            }

        return {
            "recommendation_type": "balanced_progress",
            "action": (
                f"Make steady manageable progress in {focus_area}."
            ),
            "reasoning": (
                "Current conditions support moderate consistent progress."
            )
        }