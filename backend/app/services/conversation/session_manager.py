from uuid import uuid4

from app.models.conversation_models import (
    ConversationSession
)


class SessionManager:

    def __init__(self):
        self.active_sessions = {}

    def create_session(self):
        session = ConversationSession(
            session_id=str(uuid4())
        )

        self.active_sessions[
            session.session_id
        ] = session

        return session

    def get_session(
            self,
            session_id: str
    ):
        return self.active_sessions.get(
            session_id
        )

    def update_interaction_count(
            self,
            session_id: str
    ):
        session = self.get_session(
            session_id
        )

        if session:
            session.interaction_count += 1

            return session

        return None