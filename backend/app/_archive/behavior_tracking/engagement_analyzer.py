class EngagementAnalyzer:

    def evaluate_engagement(
            self,
            interaction_count: int
    ):

        if interaction_count >= 20:
            return {
                "engagement_state": (
                    "high_engagement"
                )
            }

        if interaction_count >= 10:
            return {
                "engagement_state": (
                    "moderate_engagement"
                )
            }

        return {
            "engagement_state": (
                "early_engagement"
            )
        }