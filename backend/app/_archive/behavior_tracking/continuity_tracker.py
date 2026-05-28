from datetime import datetime, UTC

from app.models.behavior_tracking_models import (
    ContinuityRecord
)


class ContinuityTracker:

    def __init__(self):
        self.record = (
            ContinuityRecord()
        )

    def update_interaction(self):
        self.record.interaction_count += 1

        self.record.last_interaction_at = (
            datetime.now(UTC)
        )

    def get_continuity_record(self):
        return self.record