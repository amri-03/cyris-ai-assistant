from app.services.ai.context_injector import (
    ContextInjector
)

from app.services.ai.prompt_builder import (
    PromptBuilder
)

from app.services.ai.prompt_validation import (
    PromptValidation
)


class PromptCoordinator:

    def __init__(self):
        self.context_injector = (
            ContextInjector()
        )

        self.prompt_builder = (
            PromptBuilder()
        )

        self.validation = (
            PromptValidation()
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

        validation = (
            self.validation
            .validate_prompt(
                prompt
            )
        )

        return {
            "context": context,

            "prompt": prompt,

            "validation": validation
        }

    def build_prompt_summary(
            self,
            coordinated_prompt
    ):
        return {
            "prompt_integrity": (
                coordinated_prompt[
                    "validation"
                ][
                    "prompt_integrity"
                ]
            ),

            "context_sections": (
                list(
                    coordinated_prompt[
                        "context"
                    ].keys()
                )
            ),

            "prompt_preview": (
                coordinated_prompt[
                    "prompt"
                ][:120]
            )
        }