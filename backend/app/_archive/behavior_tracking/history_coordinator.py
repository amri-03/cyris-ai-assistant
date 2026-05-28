from app.services.behavior_tracking.memory_weighting import (
    MemoryWeighting
)


class HistoryCoordinator:

    def __init__(self):
        self.memory_weighting = (
            MemoryWeighting()
        )

    def coordinate_behavior_history(
            self,
            behavior_history
    ):
        history_size = len(
            behavior_history
        )

        weighting = (
            self.memory_weighting
            .evaluate_signal_weight(
                history_size
            )
        )

        return {
            "history_size": (
                history_size
            ),

            "memory_weighting": (
                weighting
            )
        }