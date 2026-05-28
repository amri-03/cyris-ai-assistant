class PromptBuilder:

    def build_prompt(
            self,
            runtime_summary,
            conversation_summary,
            behavioral_summary
    ):
        return f"""
Runtime Summary:
{runtime_summary}

Conversation Summary:
{conversation_summary}

Behavioral Summary:
{behavioral_summary}

Respond as Cyris AI Assistant with adaptive,
clear, continuity-aware guidance.
"""