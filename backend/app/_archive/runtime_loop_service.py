from app.services.runtime_scheduler_service import (
    RuntimeSchedulerService
)


class RuntimeLoopService:

    def __init__(self):
        self.scheduler_service = (
            RuntimeSchedulerService()
        )

    def execute_loop(
            self,
            cycles: int = 3
    ):
        results = []

        for cycle in range(cycles):
            result = (
                self.scheduler_service
                .schedule_runtime_cycle()
            )

            results.append({
                "cycle_number": cycle + 1,
                "result": result
            })

        return {
            "loop_status": "completed",
            "total_cycles": cycles,
            "results": results
        }