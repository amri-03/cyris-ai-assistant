class StabilityService:

    def calculate_stability(
            self,
            continuity_score: int,
            overload_detected: bool,
            inactivity_days: int,
            fragmentation_level: str
    ):

        score = continuity_score

        if overload_detected:
            score -= 2

        if inactivity_days >= 5:
            score -= 2

        if fragmentation_level == "high":
            score -= 1

        if score <= 1:
            return {
                "stability_state": "unstable",
                "stability_score": score
            }

        if score <= 4:
            return {
                "stability_state": "moderate",
                "stability_score": score
            }

        return {
            "stability_state": "stable",
            "stability_score": score
        }