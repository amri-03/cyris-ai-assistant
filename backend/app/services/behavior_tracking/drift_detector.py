class DriftDetector:

    def detect_focus_drift(
            self,
            focus_switch_count: int
    ):

        if focus_switch_count >= 10:
            return {
                "focus_state": (
                    "high_focus_drift"
                )
            }

        if focus_switch_count >= 5:
            return {
                "focus_state": (
                    "moderate_focus_drift"
                )
            }

        return {
            "focus_state": (
                "stable_focus_behavior"
            )
        }