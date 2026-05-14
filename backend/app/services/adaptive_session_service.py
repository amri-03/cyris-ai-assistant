from app.behavior.behavior_tracker import BehaviorTracker
from app.behavior.priority_engine import PriorityEngine
from app.context.context_manager import ContextManager
from app.services.assistant_service import AssistantService
from app.services.state_service import StateService

from app.models.behavior_event import BehaviorEvent
from app.models.context_state import ContextState
from app.models.priority_state import PriorityState
from app.models.user_profile import UserProfile


class AdaptiveSessionService:

    def __init__(self):
        self.behavior_tracker = BehaviorTracker()
        self.priority_engine = PriorityEngine()
        self.context_manager = ContextManager()
        self.assistant_service = AssistantService()
        self.state_service = StateService()

    def run_adaptive_session(self):
        user = UserProfile(
            name="Aman",
            long_term_goals=[
                "Build adaptive AI systems"
            ],
            active_focus_areas=[
                "Backend Development",
                "Behavioral Intelligence"
            ]
        )

        context = ContextState(
            workload_level="high",
            energy_level="low",
            available_time="medium"
        )

        priorities = PriorityState(
            high_priority=["Backend Development"],
            medium_priority=["Cybersecurity"],
            low_priority=["Blender"]
        )

        behavior_result = self.behavior_tracker.analyze_behavior(
            BehaviorEvent(
                event_type="inactivity"
            )
        )

        context_result = self.context_manager.evaluate_context(
            context
        )

        priority_result = self.priority_engine.adjust_priorities(
            priorities=priorities,
            behavior_signal=behavior_result["priority_adjustment"],
            context_mode=context_result["mode"]
        )

        guidance = self.assistant_service.generate_guidance(
            user=user,
            context=context,
            priorities=priorities
        )

        self.state_service.record_behavior(
            behavior_result["message"]
        )

        self.state_service.record_context_change(
            context_result["recommendation"]
        )

        self.state_service.record_priority_change(
            priority_result["strategy"]
        )

        return {
            "behavior": behavior_result,
            "context": context_result,
            "priorities": priority_result,
            "guidance": guidance,
            "state_history": self.state_service.get_state_history()
        }