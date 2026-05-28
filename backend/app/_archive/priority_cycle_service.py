class PriorityCycleService:

    def cycle_priorities(
            self,
            active_priorities: list,
            overload_detected: bool,
            continuity_score: int
    ):

        if (
                overload_detected
                and len(active_priorities) > 2
        ):
            return {
                "priority_mode": "reduction",
                "active_focus": active_priorities[:1],
                "maintenance_focus": active_priorities[1:],
                "guidance": (
                    "Reduce active cognitive load temporarily "
                    "while maintaining lighter continuity elsewhere."
                )
            }

        if continuity_score >= 5:
            return {
                "priority_mode": "expansion",
                "active_focus": active_priorities[:2],
                "maintenance_focus": active_priorities[2:],
                "guidance": (
                    "Current continuity may support broader active focus."
                )
            }

        return {
            "priority_mode": "balanced",
            "active_focus": active_priorities[:2],
            "maintenance_focus": active_priorities[2:],
            "guidance": (
                "Maintain balanced focus distribution."
            )
        }