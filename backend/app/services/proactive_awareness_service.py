class ProactiveAwarenessService:

    def evaluate_proactive_state(
            self,
            continuity_score: int,
            inactivity_days: int,
            overload_detected: bool
    ):

        if inactivity_days >= 7:
            return {
                "proactive_action": "gentle_reengagement",
                "message": (
                    "Consistency appears to be drifting. "
                    "A small low-pressure re-entry task may help restore momentum."
                )
            }

        if overload_detected:
            return {
                "proactive_action": "pressure_reduction",
                "message": (
                    "Current behavioral signals suggest overload. "
                    "Reducing active complexity temporarily may help stabilize consistency."
                )
            }

        if continuity_score >= 5:
            return {
                "proactive_action": "momentum_reinforcement",
                "message": (
                    "Recent continuity appears stable. "
                    "Maintaining manageable consistency is currently more valuable than increasing intensity."
                )
            }

        return {
            "proactive_action": "observe",
            "message": (
                "No proactive intervention currently required."
            )
        }