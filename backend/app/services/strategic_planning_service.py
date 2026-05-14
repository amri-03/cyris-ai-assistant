class StrategicPlanningService:

    def generate_strategy(
            self,
            career_pressure: str,
            burnout_risk: str,
            active_focus_areas: list
    ):

        if (
                career_pressure == "high"
                and burnout_risk == "high"
        ):
            return {
                "strategy_mode": "stabilization",
                "primary_direction": active_focus_areas[0],
                "guidance": (
                    "Focus on preserving sustainable consistency "
                    "instead of aggressively expanding workload."
                )
            }

        if career_pressure == "high":
            return {
                "strategy_mode": "career_alignment",
                "primary_direction": active_focus_areas[:2],
                "guidance": (
                    "Prioritize focus areas with stronger career relevance "
                    "while minimizing fragmentation."
                )
            }

        return {
            "strategy_mode": "balanced_exploration",
            "primary_direction": active_focus_areas,
            "guidance": (
                "Current conditions allow broader exploration and experimentation."
            )
        }