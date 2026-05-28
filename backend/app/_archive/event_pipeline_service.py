from app.services.forecasting_service import ForecastingService
from app.services.recovery_service import RecoveryService
from app.services.continuity_escalation_service import (
    ContinuityEscalationService
)


class EventPipelineService:

    def __init__(self):
        self.forecasting_service = ForecastingService()

        self.recovery_service = RecoveryService()

        self.escalation_service = (
            ContinuityEscalationService()
        )

    def process_event(
            self,
            event_type: str
    ):
        if event_type == "continuity_decline":
            forecast = (
                self.forecasting_service
                .evaluate_risk_forecast(
                    continuity_score=1,
                    overload_detected=True,
                    fragmentation_level="high",
                    inactivity_days=7
                )
            )

            escalation = (
                self.escalation_service
                .evaluate_escalation(
                    continuity_score=1,
                    inactivity_days=7,
                    overload_detected=True
                )
            )

            recovery = (
                self.recovery_service
                .generate_recovery_strategy(
                    forecast=forecast["forecast"],
                    overload_detected=True,
                    continuity_score=1
                )
            )

            return {
                "forecast": forecast,
                "escalation": escalation,
                "recovery": recovery
            }

        return {
            "status": "No operational pipeline triggered."
        }