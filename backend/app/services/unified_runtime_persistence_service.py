from app.services.runtime_persistence_service import (
    RuntimePersistenceService
)

from app.services.session_persistence_service import (
    SessionPersistenceService
)


class UnifiedRuntimePersistenceService:

    def __init__(self):
        self.runtime_persistence = (
            RuntimePersistenceService()
        )

        self.session_persistence = (
            SessionPersistenceService()
        )

    def persist_runtime_state(
            self,
            runtime_history,
            system_state
    ):
        self.runtime_persistence.save_runtime_history(
            runtime_history
        )

        self.session_persistence.save_session_state(
            system_state
        )

    def restore_runtime_state(self):
        history = (
            self.runtime_persistence
            .load_runtime_history()
        )

        session_state = (
            self.session_persistence
            .load_session_state()
        )

        return {
            "history": history,
            "session_state": session_state
        }