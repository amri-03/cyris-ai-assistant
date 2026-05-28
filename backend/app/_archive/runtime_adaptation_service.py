from app.models.runtime_adaptation_record import (
    RuntimeAdaptationRecord
)


class RuntimeAdaptationService:

    def __init__(self):
        self.adaptation_history = []

    def record_adaptation(
            self,
            runtime_health: str,
            throttle_mode: str,
            runtime_priority: str
    ):
        adaptation = (
            RuntimeAdaptationRecord(
                runtime_health=runtime_health,
                throttle_mode=throttle_mode,
                runtime_priority=runtime_priority
            )
        )

        self.adaptation_history.append(
            adaptation
        )

    def get_adaptation_history(self):
        return self.adaptation_history