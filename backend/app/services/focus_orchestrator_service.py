class FocusOrchestratorService:

    def orchestrate_focus(
            self,
            career_urgency: str,
            energy_level: str,
            active_focus_areas: list
    ):

        if (
                career_urgency == "high"
                and energy_level == "low"
        ):
            return {
                "primary_focus": active_focus_areas[0],
                "secondary_focus": [],
                "maintenance_focus": active_focus_areas[1:],
                "strategy": (
                    "Reduce active cognitive load and focus "
                    "on the most career-critical direction."
                )
            }

        if career_urgency == "high":
            return {
                "primary_focus": active_focus_areas[:2],
                "secondary_focus": [],
                "maintenance_focus": active_focus_areas[2:],
                "strategy": (
                    "Prioritize career-aligned focus areas "
                    "while maintaining reduced fragmentation."
                )
            }

        return {
            "primary_focus": active_focus_areas,
            "secondary_focus": [],
            "maintenance_focus": [],
            "strategy": (
                "Current conditions allow broader exploration."
            )
        }