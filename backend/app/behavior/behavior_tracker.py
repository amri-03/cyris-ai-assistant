from app.models.behavior_event import BehaviorEvent


class BehaviorTracker:

    def analyze_behavior(
            self,
            event: BehaviorEvent
    ) -> str:

        if event.event_type == "inactivity":
            return (
                "Extended inactivity detected. "
                "Consider starting with a smaller re-entry task."
            )

        if event.event_type == "focus_session":
            return (
                "Consistent engagement detected. "
                "Momentum appears stable."
            )

        return (
            "Behavior recorded successfully."
        )