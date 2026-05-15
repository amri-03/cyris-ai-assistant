from pydantic import BaseModel
from datetime import datetime, UTC
from typing import Optional


class ConversationSession(BaseModel):
    session_id: str

    started_at: datetime = (
        datetime.now(UTC)
    )

    last_interaction_at: datetime = (
        datetime.now(UTC)
    )

    active_context: Optional[str] = None

    interaction_count: int = 0


class InteractionContext(BaseModel):
    active_topic: Optional[str] = None

    conversation_mode: str = (
        "general_interaction"
    )

    runtime_linked: bool = False

    last_updated: datetime = (
        datetime.now(UTC)
    )