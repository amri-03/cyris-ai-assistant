class ConversationValidation:

    def validate_conversation_flow(
            self,
            conversation_summary
    ):

        required_fields = [
            "session_id",
            "interaction_count",
            "conversation_mode",
            "route"
        ]

        missing_fields = []

        for field in required_fields:

            if (
                    field
                    not in conversation_summary
            ):
                missing_fields.append(
                    field
                )

        if missing_fields:
            return {
                "valid": False,

                "conversation_integrity": (
                    "conversation_flow_incomplete"
                ),

                "missing_fields": (
                    missing_fields
                )
            }

        return {
            "valid": True,

            "conversation_integrity": (
                "conversation_flow_stable"
            )
        }