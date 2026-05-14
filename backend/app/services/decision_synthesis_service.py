class DecisionSynthesisService:

    def synthesize_direction(
            self,
            lifecycle_stage: str,
            overload_detected: bool,
            alignment_status: str,
            continuity_score: int
    ):

        if (
                overload_detected
                and lifecycle_stage == "drifting"
        ):
            return {
                "decision_mode": "stabilization",
                "recommended_action": (
                    "Reduce active complexity and restore sustainable consistency."
                )
            }

        if alignment_status == "misaligned":
            return {
                "decision_mode": "realignment",
                "recommended_action": (
                    "Rebalance focus toward long-term meaningful direction."
                )
            }

        if continuity_score >= 5:
            return {
                "decision_mode": "momentum_expansion",
                "recommended_action": (
                    "Current continuity appears stable enough to support deeper progress."
                )
            }

        return {
            "decision_mode": "balanced_progress",
            "recommended_action": (
                "Maintain manageable forward progress without increasing fragmentation."
            )
        }