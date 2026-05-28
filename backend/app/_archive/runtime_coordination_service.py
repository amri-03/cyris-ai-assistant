class RuntimeCoordinationService:

    def evaluate_coordination_patterns(
            self,
            adaptation_history: list
    ):
        response_patterns = {}

        for item in adaptation_history:
            key = item.runtime_priority

            response_patterns[key] = (
                    response_patterns.get(key, 0) + 1
            )

        dominant_pattern = max(
            response_patterns,
            key=response_patterns.get,
            default="none"
        )

        return {
            "dominant_runtime_pattern": (
                dominant_pattern
            ),
            "pattern_distribution": (
                response_patterns
            )
        }