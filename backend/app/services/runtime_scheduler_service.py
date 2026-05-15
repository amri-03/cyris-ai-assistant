from app.services.execution_engine_service import ExecutionEngineService
from datetime import datetime, UTC


class RuntimeSchedulerService:

    def __init__(self):
        self.last_execution_time = None
        self.execution_engine = ExecutionEngineService()

    def schedule_runtime_cycle(self):
        self.last_execution_time = (
            datetime.now(UTC)
        )

        execution_result = (
            self.execution_engine
            .execute_runtime_cycle()
        )

        return {
            "scheduler_status": (
                "runtime_cycle_executed"
            ),
            "last_execution_time": (
                self.last_execution_time
            ),
            "execution_result": execution_result
        }