class AdaptiveGuidanceEngine:

    def generate_adaptive_guidance(
            self,
            persistent_identity: list,
            behavioral_patterns: list,
            adaptive_priorities: list,
            energy_level: str
    ):

        if (
                "Recurring disengagement during overload periods"
                in behavioral_patterns
        ):
            return {
                "guidance_mode": "stability_support",
                "recommendation": (
                    "Avoid expanding active responsibilities right now. "
                    "Focus on restoring consistency gradually."
                )
            }

        if (
                "Values long-term growth"
                in persistent_identity
                and energy_level == "high"
        ):
            return {
                "guidance_mode": "growth_alignment",
                "recommendation": (
                    f"Current conditions support meaningful progress in "
                    f"{adaptive_priorities[0]}."
                )
            }

        return {
            "guidance_mode": "balanced_progress",
            "recommendation": (
                "Maintain manageable forward progress without increasing overload."
            )
        }