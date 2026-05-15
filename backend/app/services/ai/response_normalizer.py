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

        try:

            content = (
                response
                .choices[0]
                .message
                .content
            )

            return {
                "status": "success",

                "content": content
            }

        except Exception as error:

            return {
                "status": "failure",

                "error": str(error)
            }