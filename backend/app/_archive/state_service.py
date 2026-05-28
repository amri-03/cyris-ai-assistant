from app.models.state_history import StateHistory


class StateService:

    def __init__(self):
        self.state_history = StateHistory()

    def record_behavior(
            self,
            event: str
    ):
        self.state_history.behavior_events.append(event)

    def record_context_change(
            self,
            change: str
    ):
        self.state_history.context_changes.append(change)

    def record_priority_change(
            self,
            change: str
    ):
        self.state_history.priority_changes.append(change)

    def get_state_history(self):
        return self.state_history