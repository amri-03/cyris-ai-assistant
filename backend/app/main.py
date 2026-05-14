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