import os
from groq import Groq

from app.services.ai.system_prompt_manager import (
    SystemPromptManager
)


class GroqClient:

    def __init__(self):
        self.api_key = os.getenv(
            "GROQ_API_KEY"
        )

        self.system_prompt_manager = (
            SystemPromptManager()
        )

        self.client = None

        if self.api_key:
            self.client = Groq(
                api_key=self.api_key
            )

    def generate_response(
            self,
            prompt: str,
            model: str = "llama-3.1-8b-instant"
    ):
        if not self.client:
            return {
                "status": "failure",
                "error": (
                    "GROQ_API_KEY not configured."
                )
            }

        try:
            response = (
                self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                self.system_prompt_manager
                                .build_system_prompt()
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
            )

            return response

        except Exception as error:
            return {
                "status": "failure",
                "error": str(error)
            }