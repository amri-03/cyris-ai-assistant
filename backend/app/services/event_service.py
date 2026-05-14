from datetime import datetime

from app.models.behavior_event import BehaviorEvent


class EventService:

    def create_event(
            self,
            event_type: str,
            description: str,
            severity: str
    ):
        return BehaviorEvent(
            event_type=event_type,
            description=description,
            timestamp=datetime.utcnow(),
            severity=severity
        )