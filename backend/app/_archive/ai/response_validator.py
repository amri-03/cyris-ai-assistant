class ResponseValidator:

    def validate_response(
            self,
            response
    ):

        required_fields = [
            "status"
        ]

        missing_fields = []

        for field in required_fields:

            if (
                    field
                    not in response
            ):
                missing_fields.append(
                    field
                )

        if missing_fields:
            return {
                "valid": False,

                "response_integrity": (
                    "response_structure_incomplete"
                ),

                "missing_fields": (
                    missing_fields
                )
            }

        return {
            "valid": True,

            "response_integrity": (
                "response_structure_stable"
            )
        }