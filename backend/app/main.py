from fastapi import FastAPI

from app.models.user_profile import UserProfile
from app.models.context_state import ContextState
from app.models.priority_state import PriorityState
from app.models.behavior_event import BehaviorEvent

from app.behavior.behavior_tracker import BehaviorTracker
from app.behavior.priority_engine import PriorityEngine

from app.services.assistant_service import AssistantService
from app.services.state_service import StateService
from app.services.adaptive_session_service import AdaptiveSessionService
from app.services.lifecycle_service import LifecycleService
from app.services.pattern_analysis_service import PatternAnalysisService
from app.services.intervention_service import InterventionService
from app.services.focus_orchestrator_service import FocusOrchestratorService
from app.services.recommendation_service import RecommendationService
from app.services.session_continuity_service import SessionContinuityService
from app.services.memory_classification_service import MemoryClassificationService
from app.services.adaptive_guidance_engine import AdaptiveGuidanceEngine
from app.services.proactive_awareness_service import ProactiveAwarenessService
from app.services.strategic_planning_service import StrategicPlanningService
from app.services.reflection_service import ReflectionService
from app.services.alignment_engine import AlignmentEngine
from app.services.decision_synthesis_service import DecisionSynthesisService
from app.services.forecasting_service import ForecastingService
from app.services.recovery_service import RecoveryService
from app.services.adaptive_coordination_service import AdaptiveCoordinationService
from app.services.stability_service import StabilityService
from app.services.focus_state_service import FocusStateService
from app.services.priority_cycle_service import PriorityCycleService
from app.services.continuity_escalation_service import ContinuityEscalationService
from app.services.behavioral_orchestrator_service import BehavioralOrchestratorService


from app.memory.memory_manager import MemoryManager
from app.context.context_manager import ContextManager

app = FastAPI()

assistant = AssistantService()
behavior_tracker = BehaviorTracker()
memory_manager = MemoryManager()
context_manager = ContextManager()
priority_engine = PriorityEngine()
state_service = StateService()
adaptive_session_service = AdaptiveSessionService()
lifecycle_service = LifecycleService()
pattern_analysis_service = PatternAnalysisService()
intervention_service = InterventionService()
focus_orchestrator_service = FocusOrchestratorService()
recommendation_service = RecommendationService()
session_continuity_service = SessionContinuityService()
memory_classification_service = MemoryClassificationService()
adaptive_guidance_engine = AdaptiveGuidanceEngine()
proactive_awareness_service = ProactiveAwarenessService()
strategic_planning_service = StrategicPlanningService()
reflection_service = ReflectionService()
alignment_engine = AlignmentEngine()
decision_synthesis_service = DecisionSynthesisService()
recovery_service = RecoveryService()
adaptive_coordination_service = AdaptiveCoordinationService()
stability_service = StabilityService()
focus_state_service = FocusStateService()
priority_cycle_service = PriorityCycleService()
continuity_escalation_service = ContinuityEscalationService()
behavioral_orchestrator_service = BehavioralOrchestratorService()


@app.get("/")
def root():
    return {"message": "Axis AI Assistant backend is running"}


@app.get("/guidance")
def guidance():
    sample_user = UserProfile(
        name="Aman",
        long_term_goals=[
            "Become financially independent through technology"
        ],
        active_focus_areas=[
            "Web Development",
            "Cybersecurity"
        ]
    )

    sample_context = ContextState(
        energy_level="low",
        current_priority="Web Development"
    )

    sample_priorities = PriorityState(
        high_priority=["Web Development"]
    )

    result = assistant.generate_guidance(
        user=sample_user,
        context=sample_context,
        priorities=sample_priorities
    )

    return {
        "guidance": result
    }


@app.get("/behavior")
def behavior():

    sample_event = BehaviorEvent(
        event_type="inactivity",
        focus_area="Web Development",
        engagement_level=2,
        notes="No progress reported for several days"
    )

    result = behavior_tracker.analyze_behavior(
        event=sample_event
    )

    return result


@app.get("/memory")
def memory():
    sample_user = UserProfile(
        name="Aman",
        long_term_goals=[
            "Build adaptive AI systems"
        ],
        active_focus_areas=[
            "Backend Development",
            "Behavioral Intelligence"
        ]
    )

    save_result = memory_manager.save_user_profile(
        sample_user
    )

    retrieved_user = memory_manager.get_user_profile(
        "Aman"
    )

    return {
        "save_status": save_result,
        "retrieved_user": retrieved_user
    }


@app.get("/context")
def context():
    sample_context = ContextState(
        workload_level="high",
        energy_level="low",
        available_time="medium"
    )

    result = context_manager.evaluate_context(
        sample_context
    )

    return result


@app.get("/priority")
def priority():
    sample_priorities = PriorityState(
        high_priority=["Web Development"],
        medium_priority=["Cybersecurity"],
        low_priority=["Blender"]
    )

    behavior_result = behavior_tracker.analyze_behavior(
        BehaviorEvent(
            event_type="inactivity"
        )
    )

    context_result = context_manager.evaluate_context(
        ContextState(
            workload_level="high"
        )
    )

    result = priority_engine.adjust_priorities(
        priorities=sample_priorities,
        behavior_signal=behavior_result["priority_adjustment"],
        context_mode=context_result["mode"]
    )

    return result


@app.get("/state")
def state():
    state_service.record_behavior(
        "Repeated inactivity detected"
    )

    state_service.record_context_change(
        "High workload period"
    )

    state_service.record_priority_change(
        "Reduced complexity mode activated"
    )

    history = state_service.get_state_history()

    return history


@app.get("/adaptive-session")
def adaptive_session():
    result = adaptive_session_service.run_adaptive_session()

    return result


@app.get("/lifecycle")
def lifecycle():
    result = lifecycle_service.evaluate_lifecycle_state(
        inactivity_days=6,
        focus_area="Backend Development"
    )

    return result


@app.get("/patterns")
def patterns():
    result = pattern_analysis_service.analyze_patterns(
        inactivity_events=4,
        overload_events=2,
        focus_switches=5
    )

    return result


@app.get("/intervention")
def intervention():
    lifecycle_result = lifecycle_service.evaluate_lifecycle_state(
        inactivity_days=8,
        focus_area="Backend Development"
    )

    pattern_result = pattern_analysis_service.analyze_patterns(
        inactivity_events=4,
        overload_events=2,
        focus_switches=5
    )

    result = intervention_service.evaluate_intervention(
        lifecycle_stage=lifecycle_result.current_stage,
        detected_patterns=pattern_result["detected_patterns"]
    )

    return result


@app.get("/focus")
def focus():
    result = focus_orchestrator_service.orchestrate_focus(
        career_urgency="high",
        energy_level="low",
        active_focus_areas=[
            "Backend Development",
            "Cybersecurity",
            "Blender",
            "UI Design"
        ]
    )

    return result


@app.get("/recommendation")
def recommendation():
    focus_result = focus_orchestrator_service.orchestrate_focus(
        career_urgency="high",
        energy_level="low",
        active_focus_areas=[
            "Backend Development",
            "Cybersecurity",
            "Blender"
        ]
    )

    primary_focus = focus_result["primary_focus"]

    if isinstance(primary_focus, list):
        selected_focus = primary_focus[0]
    else:
        selected_focus = primary_focus

    result = recommendation_service.generate_recommendation(
        focus_area=selected_focus,
        energy_level="low",
        available_time="short"
    )

    return result


@app.get("/session-continuity")
def session_continuity():
    recommendation_result = recommendation_service.generate_recommendation(
        focus_area="Backend Development",
        energy_level="low",
        available_time="short"
    )

    session_continuity_service.update_session(
        focus_area="Backend Development",
        recommendation=recommendation_result["action"],
        continuity_change=1,
        status="recovering"
    )

    return session_continuity_service.get_session_state()


@app.get("/memory-classification")
def memory_classification():
    result = memory_classification_service.classify_memory(
        identity_traits=[
            "Strong interest in adaptive AI systems",
            "Values long-term growth"
        ],
        temporary_states=[
            "Currently experiencing workload pressure"
        ],
        patterns=[
            "Recurring disengagement during overload periods"
        ],
        priorities=[
            "Backend Development",
            "Behavioral Intelligence"
        ]
    )

    return result


@app.get("/adaptive-guidance")
def adaptive_guidance():
    memory_result = memory_classification_service.classify_memory(
        identity_traits=[
            "Strong interest in adaptive AI systems",
            "Values long-term growth"
        ],
        temporary_states=[
            "Currently experiencing workload pressure"
        ],
        patterns=[
            "Recurring disengagement during overload periods"
        ],
        priorities=[
            "Backend Development",
            "Behavioral Intelligence"
        ]
    )

    result = adaptive_guidance_engine.generate_adaptive_guidance(
        persistent_identity=memory_result.persistent_identity,
        behavioral_patterns=memory_result.behavioral_patterns,
        adaptive_priorities=memory_result.adaptive_priorities,
        energy_level="low"
    )

    return result


@app.get("/proactive-awareness")
def proactive_awareness():
    result = proactive_awareness_service.evaluate_proactive_state(
        continuity_score=3,
        inactivity_days=8,
        overload_detected=True
    )

    return result


@app.get("/strategy")
def strategy():
    result = strategic_planning_service.generate_strategy(
        career_pressure="high",
        burnout_risk="high",
        active_focus_areas=[
            "Backend Development",
            "Behavioral Intelligence",
            "Cybersecurity",
            "UI Design"
        ]
    )

    return result


@app.get("/reflection")
def reflection():
    result = reflection_service.evaluate_guidance_effectiveness(
        recommendation_followed=False,
        continuity_change=-1,
        overload_detected=True
    )

    return result


@app.get("/alignment")
def alignment():
    result = alignment_engine.evaluate_alignment(
        long_term_goal="Backend Development",
        current_focus=[
            "Backend Development",
            "Cybersecurity",
            "UI Design",
            "Blender"
        ],
        fragmentation_level="high"
    )

    return result


@app.get("/decision")
def decision():
    result = decision_synthesis_service.synthesize_direction(
        lifecycle_stage="drifting",
        overload_detected=True,
        alignment_status="aligned",
        continuity_score=2
    )

    return result


@app.get("/forecast")
def forecast():
    result = forecasting_service.evaluate_risk_forecast(
        continuity_score=2,
        overload_detected=True,
        fragmentation_level="high",
        inactivity_days=6
    )

    return result


@app.get("/recovery")
def recovery():
    result = recovery_service.generate_recovery_strategy(
        forecast="high_drift_risk",
        overload_detected=True,
        continuity_score=1
    )

    return result


@app.get("/adaptive-coordination")
def adaptive_coordination():
    result = (
        adaptive_coordination_service
        .coordinate_adaptive_response()
    )

    return result


@app.get("/stability")
def stability():
    result = stability_service.calculate_stability(
        continuity_score=3,
        overload_detected=True,
        inactivity_days=6,
        fragmentation_level="high"
    )

    return result


@app.get("/focus-state")
def focus_state():
    stability_result = stability_service.calculate_stability(
        continuity_score=2,
        overload_detected=True,
        inactivity_days=6,
        fragmentation_level="high"
    )

    result = focus_state_service.evaluate_focus_transition(
        stability_state=stability_result["stability_state"],
        continuity_score=2,
        overload_detected=True
    )

    return result


@app.get("/priority-cycle")
def priority_cycle():
    result = priority_cycle_service.cycle_priorities(
        active_priorities=[
            "Backend Development",
            "Cybersecurity",
            "UI Design",
            "Blender"
        ],
        overload_detected=True,
        continuity_score=2
    )

    return result


@app.get("/continuity-escalation")
def continuity_escalation():
    result = continuity_escalation_service.evaluate_escalation(
        continuity_score=1,
        inactivity_days=8,
        overload_detected=True
    )

    return result


@app.get("/behavioral-orchestrator")
def behavioral_orchestrator():
    result = (
        behavioral_orchestrator_service
        .orchestrate_behavioral_state()
    )

    return result


