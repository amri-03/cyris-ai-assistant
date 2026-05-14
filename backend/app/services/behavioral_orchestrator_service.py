from app.services.stability_service import StabilityService
from app.services.forecasting_service import ForecastingService
from app.services.recovery_service import RecoveryService
from app.services.focus_state_service import FocusStateService
from app.services.alignment_engine import AlignmentEngine
from app.services.continuity_escalation_service import (
    ContinuityEscalationService
)


class BehavioralOrchestratorService:

    def __init__(self):
        self.stability_service = StabilityService()
        self.forecasting_service = ForecastingService()
        self.recovery_service = RecoveryService()
        self.focus_state_service = FocusStateService()
        self.alignment_engine = AlignmentEngine()
        self.escalation_service = (
            ContinuityEscalationService()
        )

    def orchestrate_behavioral_state(self):
        stability = (
            self.stability_service.calculate_stability(
                continuity_score=2,
                overload_detected=True,
                inactivity_days=7,
                fragmentation_level="high"
            )
        )

        forecast = (
            self.forecasting_service.evaluate_risk_forecast(
                continuity_score=2,
                overload_detected=True,
                fragmentation_level="high",
                inactivity_days=7
            )
        )

        recovery = (
            self.recovery_service.generate_recovery_strategy(
                forecast=forecast["forecast"],
                overload_detected=True,
                continuity_score=2
            )
        )

        focus_state = (
            self.focus_state_service.evaluate_focus_transition(
                stability_state=stability["stability_state"],
                continuity_score=2,
                overload_detected=True
            )
        )

        alignment = (
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

        escalation = (
            self.escalation_service.evaluate_escalation(
                continuity_score=2,
                inactivity_days=7,
                overload_detected=True
            )
        )

        return {
            "stability": stability,
            "forecast": forecast,
            "recovery": recovery,
            "focus_state": focus_state,
            "alignment": alignment,
            "escalation": escalation
        }