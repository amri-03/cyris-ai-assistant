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

            if user.active_focus_areas:
                return (
                    f"Energy levels appear low right now. "
                    f"Consider making small progress in "
                    f"{user.active_focus_areas[0]} instead of deep work."
                )

            return (
                "Energy levels appear low right now. "
                "Focus on a smaller and easier task."
            )

        if priorities.high_priority:
            return (
                f"Your current highest priority focus area is "
                f"{priorities.high_priority[0]}."
            )

        if user.long_term_goals:
            return (
                f"Your long-term direction remains connected to: "
                f"{user.long_term_goals[0]}"
            )

        return (
            "No strong priority detected right now. "
            "Consider reviewing your active focus areas."
        )