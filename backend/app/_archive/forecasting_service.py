class ForecastingService:

    def evaluate_risk_forecast(
            self,
            continuity_score: int,
            overload_detected: bool,
            fragmentation_level: str,
            inactivity_days: int
    ):

        if (
                overload_detected
                and fragmentation_level == "high"
                and inactivity_days >= 5
        ):
            return {
                "forecast": "high_drift_risk",
                "guidance": (
                    "Current behavioral signals suggest elevated risk "
                    "of continuity decline if complexity remains unchanged."
                )
            }

        if continuity_score >= 5:
            return {
                "forecast": "stable_momentum",
                "guidance": (
                    "Current continuity signals appear reasonably stable."
                )
            }

        return {
            "forecast": "moderate_variability",
            "guidance": (
                "Behavioral continuity currently appears moderately unstable."
            )
        }