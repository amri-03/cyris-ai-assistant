from app.services.event_service import EventService
from app.services.event_pipeline_service import EventPipelineService
from app.services.behavioral_orchestrator_service import BehavioralOrchestratorService


class ExecutionEngineService:

    def __init__(self):
        self.event_service = EventService()

        self.pipeline_service = (
            EventPipelineService()
        )

        self.orchestrator_service = (
            BehavioralOrchestratorService()
        )

    def execute_runtime_cycle(self):
        event = self.event_service.create_event(
            event_type="continuity_decline",
            description=(
                "Operational runtime detected continuity instability."
            ),
            severity="moderate"
        )

        pipeline_result = (
            self.pipeline_service.process_event(
                event.event_type
            )
        )

        orchestration = (
            self.orchestrator_service
            .orchestrate_behavioral_state()
        )

        return {
            "event": event,
            "pipeline": pipeline_result,
            "orchestration": orchestration
        }