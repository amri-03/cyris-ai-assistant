class RuntimePredictionService:

    def predict_runtime_risk(
            self,
            adaptation_history: list
    ):

        stressed_count = sum(
            1
            for item in adaptation_history
            if item.runtime_health == "stressed"
        )

        if stressed_count >= 3:
            return {
                "runtime_prediction": (
                    "high_runtime_instability_risk"
                ),
                "guidance": (
                    "Persistent runtime stress patterns detected."
                )
            }

        if stressed_count >= 1:
            return {
                "runtime_prediction": (
                    "moderate_runtime_instability_risk"
                ),
                "guidance": (
                    "Runtime stress indicators are emerging."
                )
            }

        return {
            "runtime_prediction": (
                "stable_runtime_projection"
            ),
            "guidance": (
                "Runtime orchestration appears sustainable."
            )
        }