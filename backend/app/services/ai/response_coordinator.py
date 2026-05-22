from app.services.ai.response_validator import (
    ResponseValidator
)

from app.services.ai.response_summary_builder import (
    ResponseSummaryBuilder
)

from app.services.adaptive_response_refiner import (
    AdaptiveResponseRefiner
)

class ResponseCoordinator:

    def __init__(self):
        self.validator = (
            ResponseValidator()
        )

        self.summary_builder = (
            ResponseSummaryBuilder()
        )

        self.refiner = (
            AdaptiveResponseRefiner()
        )

    def coordinate_response(
            self,
            response
    ):
        if (
                response["status"]
                != "success"
        ):
            return {
                "response": response,
                "summary": {
                    "response_status":
                        "failure",

                    "response_preview":
                        ""
                }
            }

        refined_response = (
            self.refiner
            .refine_response(
                response["response"]
            )
        )

        return {
            "response": {
                "status": "success",
                "response": refined_response
            },

            "summary": {
                "response_status":
                    "success",

                "response_preview":
                    refined_response[:80]
            }
        }