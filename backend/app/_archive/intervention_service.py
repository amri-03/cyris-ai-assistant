class InterventionService:

    def evaluate_intervention(
            self,
            lifecycle_stage: str,
            detected_patterns: list
    ):

        if lifecycle_stage == "drifting":
            return {
                "intervention_level": "moderate",
                "guidance_style": "gentle_reentry",
                "message": (
                    "A gradual return to progress may be more "
                    "effective than attempting intense recovery."
                )
            }

        if (
                "Repeated overload periods detected."
                in detected_patterns
        ):
            return {
                "intervention_level": "light",
                "guidance_style": "pressure_reduction",
                "message": (
                    "Current conditions suggest reducing workload "
                    "pressure temporarily."
                )
            }

        if lifecycle_stage == "engaged":
            return {
                "intervention_level": "minimal",
                "guidance_style": "momentum_support",
                "message": (
                    "Momentum currently appears stable. "
                    "Maintain consistent manageable progress."
                )
            }

        return {
            "intervention_level": "neutral",
            "guidance_style": "observation",
            "message": (
                "No major intervention currently required."
            )
        }