class StateTransitionService:

    def evaluate_transition(
            self,
            continuity_score: int,
            overload_detected: bool,
            inactivity_days: int
    ):

        if (
                overload_detected
                and inactivity_days >= 5
        ):
            return {
                "next_focus_state": "recovery"
            }

        if continuity_score >= 5:
            return {
                "next_focus_state": "expansion"
            }

        if continuity_score <= 2:
            return {
                "next_focus_state": "stabilization"
            }

        return {
            "next_focus_state": "maintenance"
        }