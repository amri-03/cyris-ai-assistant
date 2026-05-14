class RuntimeTrendService:

    def analyze_trends(
            self,
            history: list
    ):

        if len(history) < 2:
            return {
                "trend_state": "insufficient_data"
            }

        latest = history[-1]

        previous = history[-2]

        if (
                latest.continuity_score >
                previous.continuity_score
        ):
            return {
                "trend_state": "improving",
                "guidance": (
                    "Behavioral continuity appears to be improving."
                )
            }

        if (
                latest.continuity_score <
                previous.continuity_score
        ):
            return {
                "trend_state": "declining",
                "guidance": (
                    "Behavioral continuity appears to be weakening."
                )
            }

        return {
            "trend_state": "stable",
            "guidance": (
                "Behavioral continuity appears relatively stable."
            )
        }