import os
import google.generativeai as genai


class GeminiClient:

    def __init__(self):
        self.api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        self.model = None

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                "gemini-1.5-flash"
            )

    def generate_response(
            self,
            prompt: str
    ):
        if not self.model:
            return {
                "status": "failure",
                "error": (
                    "GEMINI_API_KEY not configured."
                )
            }

        try:
            response = self.model.generate_content(
                prompt
            )

            return response

        except Exception as error:
            return {
                "status": "failure",
                "error": str(error)
            }