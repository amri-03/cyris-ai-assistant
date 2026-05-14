from app.models.system_state import SystemState


class StateEngineService:

    def __init__(self):
        self.system_state = SystemState()

    def update_state(
            self,
            continuity_score: int,
            overload_detected: bool,
            fragmentation_level: str,
            inactivity_days: int,
            focus_state: str,
            escalation_level: str
    ):
        self.system_state.continuity_score = (
            continuity_score
        )

        self.system_state.overload_detected = (
            overload_detected
        )

        self.system_state.fragmentation_level = (
            fragmentation_level
        )

        self.system_state.inactivity_days = (
            inactivity_days
        )

        self.system_state.current_focus_state = (
            focus_state
        )

        self.system_state.escalation_level = (
            escalation_level
        )

    def get_state(self):
        return self.system_state