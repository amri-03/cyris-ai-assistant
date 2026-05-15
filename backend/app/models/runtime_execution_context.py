from pydantic import BaseModel


class RuntimeExecutionContext(BaseModel):
    orchestration: dict

    runtime_health: dict

    throttle: dict

    adaptation_history: list