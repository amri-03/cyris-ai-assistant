class RecoveryService:

    def generate_recovery_strategy(
            self,
            forecast: str,
            overload_detected: bool,
            continuity_score: int
    ):

        if (
                forecast == "high_drift_risk"
                and overload_detected
        ):
            return {
                "recovery_mode": "stabilization",
                "strategy": (
                    "Reduce active focus areas and rebuild "
                    "consistency through smaller achievable sessions."
                )
            }

        if continuity_score <= 2:
            return {
                "recovery_mode": "low_pressure_reentry",
                "strategy": (
                    "Re-enter progress gradually using lightweight "
                    "manageable tasks."
                )
            }

        return {
            "recovery_mode": "maintenance",
            "strategy": (
                "Maintain steady manageable progress."
            )
        }