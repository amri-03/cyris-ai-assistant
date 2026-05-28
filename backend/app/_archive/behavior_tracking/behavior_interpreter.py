from app.services.behavior_tracking.engagement_analyzer import (
    EngagementAnalyzer
)

from app.services.behavior_tracking.drift_detector import (
    DriftDetector
)

from app.services.behavior_tracking.behavior_validation import (
    BehaviorValidation
)


class BehaviorInterpreter:

    def __init__(self):
        self.engagement_analyzer = (
            EngagementAnalyzer()
        )

        self.drift_detector = (
            DriftDetector()
        )

        self.validation = (
            BehaviorValidation()
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

        analysis = {
            "engagement_analysis": (
                engagement
            ),

            "focus_analysis": (
                drift
            )
        }

        validation = (
            self.validation
            .validate_behavior_analysis(
                analysis
            )
        )

        return {
            "behavior_analysis": (
                analysis
            ),

            "validation": (
                validation
            )
        }

    def build_behavior_summary(
            self,
            behavior_analysis
    ):
        return {
            "engagement_state": (
                behavior_analysis[
                    "behavior_analysis"
                ][
                    "engagement_analysis"
                ][
                    "engagement_state"
                ]
            ),

            "focus_state": (
                behavior_analysis[
                    "behavior_analysis"
                ][
                    "focus_analysis"
                ][
                    "focus_state"
                ]
            ),

            "behavior_integrity": (
                behavior_analysis[
                    "validation"
                ][
                    "behavior_integrity"
                ]
            )
        }