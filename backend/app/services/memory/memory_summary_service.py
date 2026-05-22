class MemorySummaryService:

    def build_summary(
            self,
            memory_messages
    ):

        user_messages = []

        for message in memory_messages:

            if (
                    message["role"]
                    == "user"
            ):
                user_messages.append(
                    message["content"]
                )

        recent_context = (
            "\n".join(
                user_messages[-5:]
            )
        )

        return (
            "Recent user continuity:\n"
            f"{recent_context}"
        )