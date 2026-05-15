from app.models.behavior_tracking_models import (
    BehaviorSignal
)


class BehaviorEventTracker:

    def __init__(self):
        self.behavior_signals = []

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

        return signal

    def get_signals(self):
        return self.behavior_signals