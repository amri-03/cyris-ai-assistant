from app.services.forecasting_service import ForecastingService
from app.services.recovery_service import RecoveryService
from app.services.alignment_engine import AlignmentEngine
from app.services.decision_synthesis_service import DecisionSynthesisService


class AdaptiveCoordinationService:

    def __init__(self):
        self.forecasting_service = ForecastingService()
        self.recovery_service = RecoveryService()
        self.alignment_engine = AlignmentEngine()
        self.decision_service = DecisionSynthesisService()

    def coordinate_adaptive_response(self):
        forecast_result = (
            self.forecasting_service.evaluate_risk_forecast(
                continuity_score=2,
                overload_detected=True,
                fragmentation_level="high",
                inactivity_days=6
            )
        )

        alignment_result = (
            self.alignment_engine.evaluate_alignment(
                long_term_goal="Backend Development",
                current_focus=[
                    "Backend Development",
                    "Cybersecurity",
                    "UI Design",
                    "Blender"
                ],
                fragmentation_level="high"
            )
        )

        decision_result = (
            self.decision_service.synthesize_direction(
                lifecycle_stage="drifting",
                overload_detected=True,
                alignment_status=alignment_result["alignment_status"],
                continuity_score=2
            )
        )

        recovery_result = (
            self.recovery_service.generate_recovery_strategy(
                forecast=forecast_result["forecast"],
                overload_detected=True,
                continuity_score=2
            )
        )

        return {
            "forecast": forecast_result,
            "alignment": alignment_result,
            "decision": decision_result,
            "recovery": recovery_result
        }