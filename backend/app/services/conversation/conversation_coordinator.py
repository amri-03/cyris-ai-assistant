from app.services.conversation.session_manager import (
    SessionManager
)

from app.services.conversation.interaction_state import (
    InteractionState
)


class ConversationCoordinator:

    def __init__(self):
        self.session_manager = (
            SessionManager()
        )

        self.interaction_state = (
            InteractionState()
        )

    def initialize_conversation(self):
        session = (
            self.session_manager
            .create_session()
        )

        return {
            "session": session,
            "interaction_context": (
                self.interaction_state
                .get_context()
            )
        }

    def register_interaction(
            self,
            session_id: str,
            topic: str
    ):
        session = (
            self.session_manager
            .update_interaction_count(
                session_id
            )
        )

        self.interaction_state.update_topic(
            topic
        )

        return {
            "session": session,
            "interaction_context": (
                self.interaction_state
                .get_context()
            )
        }