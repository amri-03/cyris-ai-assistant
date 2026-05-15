class RuntimeValidationService:

    def validate_runtime_state(
            self,
            runtime_state
    ):

        required_sections = [
            "operational_state",
            "analytical_state"
        ]

        missing_sections = []

        for section in required_sections:

            if section not in runtime_state:
                missing_sections.append(
                    section
                )

        if missing_sections:
            return {
                "valid": False,
                "missing_sections": (
                    missing_sections
                )
            }

        return {
            "valid": True
        }