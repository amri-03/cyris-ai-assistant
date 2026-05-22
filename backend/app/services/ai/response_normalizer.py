class ResponseNormalizer:

    def normalize_response(
            self,
            response
    ):

        if isinstance(
                response,
                dict
        ):
            return response

        # Groq (OpenAI-compatible structure)
        try:
            if hasattr(response, "choices"):
                content = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                return {
                    "status": "success",
                    "response": content
                }
        except Exception:
            pass

        # Gemini structure
        try:
            if hasattr(response, "text"):
                return {
                    "status": "success",
                    "response": response.text
                }
        except Exception:
            pass

        return {
            "status": "failure",
            "error": (
                "Unrecognized response format."
            )
        }