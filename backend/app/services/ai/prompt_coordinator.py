from app.services.ai.context_injector import (
    ContextInjector
)

from app.services.ai.prompt_builder import (
    PromptBuilder
)


class PromptCoordinator:

    def __init__(self):
        self.context_injector = (
            ContextInjector()
        )

        self.prompt_builder = (
            PromptBuilder()
        )

    def coordinate_prompt(
            self,
            runtime_summary,
            conversation_summary,
            behavioral_summary
    ):
        context = (
            self.context_injector
            .inject_context(
                runtime_summary,
                conversation_summary,
                behavioral_summary
            )
        )

        prompt = (
            self.prompt_builder
            .build_prompt(
                runtime_summary=(
                    context[
                        "runtime_summary"
                    ]
                ),

                conversation_summary=(
                    context[
                        "conversation_summary"
                    ]
                ),

                behavioral_summary=(
                    context[
                        "behavioral_summary"
                    ]
                )
            )
        )

        return {
            "context": context,
            "prompt": prompt
        }