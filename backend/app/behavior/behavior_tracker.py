from app.models.behavior_event import BehaviorEvent


class BehaviorTracker:

    def analyze_behavior(
            self,
            event: BehaviorEvent
    ) -> dict:

        if event.event_type == "inactivity":
            return {
                "status": "warning",
                "message": (
                    "Extended inactivity detected. "
                    "Consider starting with a smaller re-entry task."
                ),
                "priority_adjustment": "reduce_complexity"
            }

        if event.event_type == "focus_session":
            return {
                "status": "positive",
                "message": (
                    "Consistent engagement detected. "
                    "Momentum appears stable."
                ),
                "priority_adjustment": "maintain_progress"
            }

        return {
            "status": "neutral",
            "message": "Behavior recorded successfully.",
            "priority_adjustment": "none"
        }