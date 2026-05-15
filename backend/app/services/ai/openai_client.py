import os

from openai import OpenAI


class OpenAIClient:

    def __init__(self):

        self.api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        self.client = None

        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key
            )

    def generate_response(
            self,
            prompt: str,
            model: str = "gpt-4.1-mini"
    ):

        if not self.client:
            return {
                "status": "failure",
                "error": (
                    "OPENAI_API_KEY not configured."
                )
            }

        response = (
            self.client.chat.completions.create(
                model=model,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )

        return response