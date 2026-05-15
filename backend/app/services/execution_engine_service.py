from app.services.event_service import EventService
from app.services.event_pipeline_service import EventPipelineService
from app.services.behavioral_orchestrator_service import (
    BehavioralOrchestratorService
)
from app.services.runtime_health_service import RuntimeHealthService
from app.services.runtime_throttle_service import RuntimeThrottleService
from app.services.runtime_priority_service import RuntimePriorityService
from app.services.runtime_adaptation_service import (
    RuntimeAdaptationService
)
from app.services.runtime_strategy_service import (
    RuntimeStrategyService
)
from app.services.runtime_prediction_service import (
    RuntimePredictionService
)
from app.services.runtime_response_service import (
    RuntimeResponseService
)
from app.services.runtime_reflection_service import (
    RuntimeReflectionService
)
from app.services.runtime_coordination_service import (
    RuntimeCoordinationService
)
from app.services.runtime_decision_service import (
    RuntimeDecisionService
)
from app.services.runtime_equilibrium_service import (
    RuntimeEquilibriumService
)
from app.services.runtime_governance_service import (
    RuntimeGovernanceService
)
from app.models.runtime_execution_context import (
    RuntimeExecutionContext
)


class ExecutionEngineService:

    def __init__(self):
        self.event_service = EventService()
        self.pipeline_service = EventPipelineService()
        self.orchestrator_service = BehavioralOrchestratorService()
        self.runtime_health_service = RuntimeHealthService()
        self.runtime_throttle_service = RuntimeThrottleService()
        self.runtime_priority_service = RuntimePriorityService()
        self.runtime_adaptation_service = RuntimeAdaptationService()
        self.runtime_strategy_service = RuntimeStrategyService()
        self.runtime_prediction_service = RuntimePredictionService()
        self.runtime_response_service = RuntimeResponseService()
        self.runtime_reflection_service = RuntimeReflectionService()
        self.runtime_coordination_service = RuntimeCoordinationService()
        self.runtime_decision_service = (
            RuntimeDecisionService()
        )
        self.runtime_equilibrium_service = (
            RuntimeEquilibriumService()
        )
        self.runtime_governance_service = (
            RuntimeGovernanceService()
        )

        self.runtime_cycles = 0

    def evaluate_runtime_analysis(
            self,
            runtime_context
    ):

        strategy_evaluation = (
            self.runtime_strategy_service
            .evaluate_strategy_effectiveness(
                runtime_context.adaptation_history
            )
        )

        runtime_prediction = (
            self.runtime_prediction_service
            .predict_runtime_risk(
                runtime_context.adaptation_history
            )
        )

        runtime_reflection = (
            self.runtime_reflection_service
            .reflect_on_runtime_behavior(
                runtime_context.adaptation_history
            )
        )

        return {
            "strategy_evaluation": (
                strategy_evaluation
            ),
            "runtime_prediction": (
                runtime_prediction
            ),
            "runtime_reflection": (
                runtime_reflection
            )
        }

    def evaluate_runtime_coordination(
            self,
            runtime_context,
            runtime_prediction
    ):

        runtime_response = (
            self.runtime_response_service
            .evolve_runtime_response(
                runtime_prediction=(
                    runtime_prediction[
                        "runtime_prediction"
                    ]
                )
            )
        )

        runtime_coordination = (
            self.runtime_coordination_service
            .evaluate_coordination_patterns(
                runtime_context.adaptation_history
            )
        )

        runtime_decision = (
            self.runtime_decision_service
            .evolve_runtime_decision(
                dominant_runtime_pattern=(
                    runtime_coordination[
                        "dominant_runtime_pattern"
                    ]
                )
            )
        )

        runtime_equilibrium = (
            self.runtime_equilibrium_service
            .evaluate_runtime_equilibrium(
                runtime_context.adaptation_history
            )
        )

        runtime_governance = (
            self.runtime_governance_service
            .evaluate_runtime_governance(
                equilibrium_state=(
                    runtime_equilibrium[
                        "equilibrium_state"
                    ]
                ),
                runtime_prediction=(
                    runtime_prediction[
                        "runtime_prediction"
                    ]
                )
            )
        )

        return {
            "runtime_response": (
                runtime_response
            ),
            "runtime_coordination": (
                runtime_coordination
            ),
            "runtime_decision": (
                runtime_decision
            ),
            "runtime_equilibrium": (
                runtime_equilibrium
            ),
            "runtime_governance": (
                runtime_governance
            )
        }

    def evaluate_runtime_management(
            self,
            orchestration,
            runtime_health,
            throttle
    ):

        runtime_priority = (
            self.runtime_priority_service
            .evaluate_runtime_priority(
                runtime_health=(
                    runtime_health[
                        "runtime_health"
                    ]
                ),
                escalation_level=(
                    orchestration[
                        "escalation"
                    ]["escalation_level"]
                )
            )
        )

        self.runtime_adaptation_service.record_adaptation(
            runtime_health=(
                runtime_health[
                    "runtime_health"
                ]
            ),
            throttle_mode=(
                throttle[
                    "throttle_mode"
                ]
            ),
            runtime_priority=(
                runtime_priority[
                    "runtime_priority"
                ]
            )
        )

        adaptation_history = (
            self.runtime_adaptation_service
            .get_adaptation_history()
        )

        runtime_context = (
            RuntimeExecutionContext(
                orchestration=orchestration,
                runtime_health=runtime_health,
                throttle=throttle,
                adaptation_history=adaptation_history
            )
        )

        analysis_state = (
            self.evaluate_runtime_analysis(
                runtime_context
            )
        )

        coordination_state = (
            self.evaluate_runtime_coordination(
                runtime_context=runtime_context,
                runtime_prediction=(
                    analysis_state[
                        "runtime_prediction"
                    ]
                )
            )
        )

        execution_mode = (
            "normal_runtime_execution"
        )

        if (
                coordination_state[
                    "runtime_governance"
                ][
                    "governance_mode"
                ]
                == "runtime_rebalancing"
        ):
            execution_mode = (
                "reduced_runtime_execution"
            )

        if (
                coordination_state[
                    "runtime_governance"
                ][
                    "governance_mode"
                ]
                == "protective_runtime_control"
        ):
            execution_mode = (
                "protective_runtime_execution"
            )

        runtime_operational_state = {
            "runtime_priority": (
                runtime_priority
            ),

            "execution_mode": (
                execution_mode
            ),

            "runtime_governance": (
                coordination_state[
                    "runtime_governance"
                ]
            )
        }

        runtime_analytical_state = {
            "analysis_state": (
                analysis_state
            ),

            "coordination_state": (
                coordination_state
            )
        }

        return {
            "operational_state": (
                runtime_operational_state
            ),

            "analytical_state": (
                runtime_analytical_state
            )
        }

    def build_runtime_summary(
            self,
            runtime_state
    ):

        return {
            "runtime_priority": (
                runtime_state[
                    "operational_state"
                ][
                    "runtime_priority"
                ][
                    "runtime_priority"
                ]
            ),

            "runtime_prediction": (
                runtime_state[
                    "analytical_state"
                ][
                    "analysis_state"
                ][
                    "runtime_prediction"
                ][
                    "runtime_prediction"
                ]
            ),

            "runtime_governance": (
                runtime_state[
                    "analytical_state"
                ][
                    "coordination_state"
                ][
                    "runtime_governance"
                ][
                    "governance_mode"
                ]
            ),

            "execution_mode": (
                runtime_state[
                    "operational_state"
                ][
                    "execution_mode"
                ]
            )
        }

    def execute_runtime_cycle(self):
        event = self.event_service.create_event(
            event_type="continuity_decline",
            description=(
                "Operational runtime detected continuity instability."
            ),
            severity="moderate"
        )

        self.runtime_cycles += 1

        pipeline_result = (
            self.pipeline_service.process_event(
                event.event_type
            )
        )

        orchestration = (
            self.orchestrator_service
            .orchestrate_behavioral_state()
        )

        runtime_health = (
            self.runtime_health_service
            .evaluate_runtime_health(
                total_runtime_cycles=self.runtime_cycles,
                overload_detected=True
            )
        )

        throttle = (
            self.runtime_throttle_service
            .evaluate_throttle(
                runtime_health=runtime_health["runtime_health"]
            )
        )

        runtime_state = (
            self.evaluate_runtime_management(
                orchestration=orchestration,
                runtime_health=runtime_health,
                throttle=throttle
            )
        )

        runtime_summary = (
            self.build_runtime_summary(
                runtime_state
            )
        )

        return {
            "event": event,
            "pipeline": pipeline_result,
            "orchestration": orchestration,
            "runtime_health": runtime_health,
            "runtime_throttle": throttle,
            "runtime_state": (
                runtime_state
            ),
            "runtime_summary": (
                runtime_summary
            ),
            "governance_history": (
                self.runtime_governance_service
                .governance_memory
                .get_governance_history()
            ),
        }