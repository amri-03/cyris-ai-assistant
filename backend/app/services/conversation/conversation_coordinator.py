from app.services.conversation.session_manager import (
    SessionManager
)
from app.services.conversation.interaction_state import (
    InteractionState
)
from app.services.conversation.context_router import (
    ContextRouter
)
from app.services.conversation.conversation_runtime_bridge import (
    ConversationRuntimeBridge
)


class ConversationCoordinator:

    def __init__(self):
        self.session_manager = (
            SessionManager()
        )

        self.interaction_state = (
            InteractionState()
        )

        self.context_router = (
            ContextRouter()
        )

        self.runtime_bridge = (
            ConversationRuntimeBridge()
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

    def coordinate_runtime_conversation(
            self,
            runtime_state
    ):
        self.interaction_state.link_runtime_context()

        runtime_context = (
            self.runtime_bridge
            .build_runtime_context(
                runtime_state
            )
        )

        route = (
            self.context_router
            .determine_context_route(
                self.interaction_state
                .get_context()
            )
        )

        return {
            "runtime_context": (
                runtime_context
            ),

            "route": route,

            "interaction_context": (
                self.interaction_state
                .get_context()
            )
        }