from app.models.user_profile import UserProfile
from app.models.context_state import ContextState
from app.models.priority_state import PriorityState


class AssistantService:

    def generate_guidance(
            self,
            user: UserProfile,
            context: ContextState,
            priorities: PriorityState
    ) -> str:

        if context.energy_level == "low":
            return (
                "Energy levels appear low right now. "
                "Focus on a smaller and easier task instead of deep work."
            )

        if priorities.high_priority:
            return (
                f"Your current highest priority focus area is: "
                f"{priorities.high_priority[0]}"
            )

        return (
            "No strong priority detected right now. "
            "Consider reviewing your active focus areas."
        )
