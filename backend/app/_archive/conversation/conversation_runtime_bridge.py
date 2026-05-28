class ConversationRuntimeBridge:

    def build_runtime_context(
            self,
            runtime_state
    ):
        return {
            "runtime_summary": (
                runtime_state.get(
                    "runtime_summary"
                )
            ),

            "runtime_validation": (
                runtime_state.get(
                    "runtime_validation"
                )
            )
        }