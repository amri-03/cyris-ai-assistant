from fastapi import FastAPI

from app.models.user_profile import UserProfile
from app.models.context_state import ContextState
from app.models.priority_state import PriorityState
from app.models.behavior_event import BehaviorEvent
from app.behavior.behavior_tracker import BehaviorTracker

from app.services.assistant_service import AssistantService

app = FastAPI()

assistant = AssistantService()
behavior_tracker = BehaviorTracker()


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

    return {
        "behavior_analysis": result
    }