from app.services.ai.response_validator import (
    ResponseValidator
)

from app.services.ai.response_summary_builder import (
    ResponseSummaryBuilder
)


class ResponseCoordinator:

    def __init__(self):
        self.validator = (
            ResponseValidator()
        )

        self.summary_builder = (
            ResponseSummaryBuilder()
        )

    def coordinate_response(
            self,
            response
    ):
        validation = (
            self.validator
            .validate_response(
                response
            )
        )

        summary = (
            self.summary_builder
            .build_summary(
                response
            )
        )

        return {
            "response": response,

            "validation": validation,

            "summary": summary
        }