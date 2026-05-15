class ContextInjector:

    def inject_context(
            self,
            runtime_summary,
            conversation_summary,
            behavioral_summary
    ):
        return {
            "runtime_summary": (
                runtime_summary
            ),

            "conversation_summary": (
                conversation_summary
            ),

            "behavioral_summary": (
                behavioral_summary
            )
        }