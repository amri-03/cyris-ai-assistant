from app.models.user_lifecycle import UserLifecycle


class LifecycleService:

    def evaluate_lifecycle_state(
            self,
            inactivity_days: int,
            focus_area: str
    ) -> UserLifecycle:

        if inactivity_days >= 7:
            return UserLifecycle(
                current_stage="drifting",
                consistency_level="low",
                engagement_status="inactive",
                dominant_focus_area=focus_area,
                burnout_risk="medium",
                last_active_days_ago=inactivity_days
            )

        if inactivity_days >= 3:
            return UserLifecycle(
                current_stage="unstable",
                consistency_level="moderate",
                engagement_status="reduced",
                dominant_focus_area=focus_area,
                burnout_risk="low",
                last_active_days_ago=inactivity_days
            )

        return UserLifecycle(
            current_stage="engaged",
            consistency_level="stable",
            engagement_status="active",
            dominant_focus_area=focus_area,
            burnout_risk="low",
            last_active_days_ago=inactivity_days
        )