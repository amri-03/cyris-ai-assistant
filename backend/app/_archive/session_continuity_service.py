from app.models.session_state import SessionState


class SessionContinuityService:

    def __init__(self):
        self.session_state = SessionState()

    def update_session(
            self,
            focus_area: str,
            recommendation: str,
            continuity_change: int,
            status: str
    ):
        self.session_state.recent_focus_areas.append(
            focus_area
        )

        self.session_state.recent_recommendations.append(
            recommendation
        )

        self.session_state.continuity_score += continuity_change

        self.session_state.last_known_status = status

    def get_session_state(self):
        return self.session_state