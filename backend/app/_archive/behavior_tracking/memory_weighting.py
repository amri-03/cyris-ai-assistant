class MemoryWeighting:

    def evaluate_signal_weight(
            self,
            signal_count: int
    ):

        if signal_count >= 20:
            return {
                "memory_weight": (
                    "high_continuity"
                )
            }

        if signal_count >= 10:
            return {
                "memory_weight": (
                    "moderate_continuity"
                )
            }

        return {
            "memory_weight": (
                "early_behavioral_pattern"
            )
        }