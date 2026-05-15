from app.models.conversation_models import (
    InteractionContext
)


class InteractionState:

    def __init__(self):
        self.context = (
            InteractionContext()
        )

    def update_topic(
            self,
            topic: str
    ):
        self.context.active_topic = topic

    def update_mode(
            self,
            mode: str
    ):
        self.context.conversation_mode = (
            mode
        )

    def link_runtime_context(self):
        self.context.runtime_linked = True

    def get_context(self):
        return self.context