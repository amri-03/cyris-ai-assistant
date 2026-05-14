from app.services.stability_service import StabilityService
from app.services.forecasting_service import ForecastingService
from app.services.recovery_service import RecoveryService
from app.services.focus_state_service import FocusStateService
from app.services.alignment_engine import AlignmentEngine
from app.services.continuity_escalation_service import ContinuityEscalationService
from app.services.state_engine_service import StateEngineService
from app.services.state_transition_service import StateTransitionService
from app.services.state_history_service import StateHistoryService
from app.services.runtime_trend_service import RuntimeTrendService
from app.services.runtime_optimization_service import RuntimeOptimizationService


class BehavioralOrchestratorService:

    def __init__(self):
        self.stability_service = StabilityService()
        self.forecasting_service = ForecastingService()
        self.recovery_service = RecoveryService()
        self.focus_state_service = FocusStateService()
        self.alignment_engine = AlignmentEngine()
        self.escalation_service = ContinuityEscalationService()
        self.state_engine = StateEngineService()
        self.transition_service = StateTransitionService()
        self.history_service = StateHistoryService()
        self.trend_service = RuntimeTrendService()
        self.optimization_service = RuntimeOptimizationService()

    def orchestrate_behavioral_state(self):
        self.state_engine.update_state(
            continuity_score=2,
            overload_detected=True,
            fragmentation_level="high",
            inactivity_days=7,
            focus_state="stabilization",
            escalation_level="moderate"
        )

        current_state = self.state_engine.get_state()

        transition = (
            self.transition_service.evaluate_transition(
                continuity_score=current_state.continuity_score,
                overload_detected=current_state.overload_detected,
                inactivity_days=current_state.inactivity_days
            )
        )

        current_state.current_focus_state = (
            transition["next_focus_state"]
        )

        self.history_service.record_state(
            focus_state=current_state.current_focus_state,
            continuity_score=current_state.continuity_score,
            overload_detected=current_state.overload_detected
        )

        trend_analysis = (
            self.trend_service.analyze_trends(
                self.history_service.get_history()
            )
        )

        optimization = (
            self.optimization_service
            .optimize_runtime_behavior(
                trend_state=trend_analysis["trend_state"],
                overload_detected=current_state.overload_detected
            )
        )

        stability = (
            self.stability_service.calculate_stability(
                continuity_score=current_state.continuity_score,
                overload_detected=current_state.overload_detected,
                inactivity_days=current_state.inactivity_days,
                fragmentation_level=current_state.fragmentation_level
            )
        )

        forecast = (
            self.forecasting_service.evaluate_risk_forecast(
                continuity_score=current_state.continuity_score,
                overload_detected=current_state.overload_detected,
                fragmentation_level=current_state.fragmentation_level,
                inactivity_days=current_state.inactivity_days
            )
        )

        recovery = (
            self.recovery_service.generate_recovery_strategy(
                forecast=forecast["forecast"],
                overload_detected=current_state.overload_detected,
                continuity_score=current_state.continuity_score
            )
        )

        focus_state = (
            self.focus_state_service.evaluate_focus_transition(
                stability_state=stability["stability_state"],
                continuity_score=current_state.continuity_score,
                overload_detected=current_state.overload_detected
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
                fragmentation_level=current_state.fragmentation_level
            )
        )

        escalation = (
            self.escalation_service.evaluate_escalation(
                continuity_score=current_state.continuity_score,
                inactivity_days=current_state.inactivity_days,
                overload_detected=current_state.overload_detected
            )
        )

        return {
            "system_state": current_state,
            "transition": transition,
            "state_history": self.history_service.get_history(),
            "trend_analysis": trend_analysis,
            "optimization": optimization,
            "stability": stability,
            "forecast": forecast,
            "recovery": recovery,
            "focus_state": focus_state,
            "alignment": alignment,
            "escalation": escalation
        }