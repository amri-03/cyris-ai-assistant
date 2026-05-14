class FocusStateService:

    def evaluate_focus_transition(
            self,
            stability_state: str,
            continuity_score: int,
            overload_detected: bool
    ):

        if (
                stability_state == "unstable"
                and overload_detected
        ):
            return {
                "focus_state": "stabilization",
                "transition_guidance": (
                    "Reduce active focus areas and prioritize recovery-oriented consistency."
                )
            }

        if continuity_score >= 5:
            return {
                "focus_state": "expansion",
                "transition_guidance": (
                    "Current momentum may support deeper specialization or growth."
                )
            }

        return {
            "focus_state": "maintenance",
            "transition_guidance": (
                "Maintain steady manageable focus progression."
            )
        }