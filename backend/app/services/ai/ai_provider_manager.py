from app.services.ai.openai_client import (
    OpenAIClient
)

from app.services.ai.response_normalizer import (
    ResponseNormalizer
)


class AIProviderManager:

    def __init__(self):
        self.openai_client = (
            OpenAIClient()
        )

        self.normalizer = (
            ResponseNormalizer()
        )

    def generate_ai_response(
            self,
            prompt: str
    ):
        raw_response = (
            self.openai_client
            .generate_response(
                prompt
            )
        )

        normalized_response = (
            self.normalizer
            .normalize_response(
                raw_response
            )
        )

        return normalized_response