class ResponseSummaryBuilder:

    def build_summary(
            self,
            response
    ):
        return {
            "response_status": (
                response.get(
                    "status"
                )
            ),

            "response_preview": (
                str(
                    response.get(
                        "content",
                        ""
                    )
                )[:120]
            )
        }