from app.services.behavior_tracking.engagement_analyzer import (
    EngagementAnalyzer
)

from app.services.behavior_tracking.drift_detector import (
    DriftDetector
)


class BehaviorInterpreter:

    def __init__(self):
        self.engagement_analyzer = (
            EngagementAnalyzer()
        )

        self.drift_detector = (
            DriftDetector()
        )

    def interpret_behavior(
            self,
            interaction_count: int,
            focus_switch_count: int
    ):
        engagement = (
            self.engagement_analyzer
            .evaluate_engagement(
                interaction_count
            )
        )

        drift = (
            self.drift_detector
            .detect_focus_drift(
                focus_switch_count
            )
        )

        return {
            "engagement_analysis": (
                engagement
            ),

            "focus_analysis": (
                drift
            )
        }