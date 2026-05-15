from datetime import datetime, UTC

from app.models.runtime_state_record import RuntimeStateRecord


class StateHistoryService:

    def __init__(self):
        self.history = []

    def record_state(
            self,
            focus_state: str,
            continuity_score: int,
            overload_detected: bool
    ):
        state = RuntimeStateRecord(
            focus_state=focus_state,
            continuity_score=continuity_score,
            overload_detected=overload_detected,
            timestamp=datetime.now(UTC)
        )

        self.history.append(state)

    def get_history(self):
        return self.history

    def restore_history(
            self,
            stored_history: list
    ):
        self.history = [
            RuntimeStateRecord(**item)
            for item in stored_history
        ]