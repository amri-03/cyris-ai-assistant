from app.models.behavior_tracking_models import (
    BehaviorSignal
)

from app.services.behavior_tracking.behavior_memory_manager import (
    BehaviorMemoryManager
)


class BehaviorEventTracker:

    def __init__(self):
        self.behavior_signals = []
        self.memory_manager = (
            BehaviorMemoryManager()
        )

    def record_signal(
            self,
            signal_type: str,
            metadata=None
    ):
        signal = (
            BehaviorSignal(
                signal_type=signal_type,
                metadata=metadata
            )
        )

        self.behavior_signals.append(
            signal
        )

        self.memory_manager.store_behavior_signal(
            signal
        )

        return signal

    def get_signals(self):
        return self.behavior_signals