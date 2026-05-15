from datetime import datetime, UTC

from app.models.behavior_tracking_models import (
    FocusPattern
)


class FocusTracker:

    def __init__(self):
        self.pattern = (
            FocusPattern()
        )

    def update_focus(
            self,
            focus: str
    ):
        if (
                self.pattern.active_focus
                != focus
        ):
            self.pattern.focus_switch_count += 1

        self.pattern.active_focus = focus

        self.pattern.last_updated = (
            datetime.now(UTC)
        )

    def get_focus_pattern(self):
        return self.pattern