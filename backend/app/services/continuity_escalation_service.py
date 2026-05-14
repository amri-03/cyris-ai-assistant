class ContinuityEscalationService:

    def evaluate_escalation(
            self,
            continuity_score: int,
            inactivity_days: int,
            overload_detected: bool
    ):

        if (
                inactivity_days >= 7
                and overload_detected
        ):
            return {
                "escalation_level": "high",
                "response_mode": "recovery_intervention",
                "guidance": (
                    "Strong continuity decline detected. "
                    "Prioritize stabilization and low-pressure re-entry."
                )
            }

        if continuity_score <= 2:
            return {
                "escalation_level": "moderate",
                "response_mode": "gentle_support",
                "guidance": (
                    "Continuity instability detected. "
                    "Reduce fragmentation and restore manageable consistency."
                )
            }

        return {
            "escalation_level": "low",
            "response_mode": "passive_monitoring",
            "guidance": (
                "Current continuity appears reasonably stable."
            )
        }