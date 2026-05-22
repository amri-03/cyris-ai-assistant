import os

from app.services.ai.gemini_client import (
    GeminiClient
)

from app.services.ai.groq_client import (
    GroqClient
)

from app.services.ai.response_normalizer import (
    ResponseNormalizer
)

from app.services.ai.response_coordinator import (
    ResponseCoordinator
)


class AIProviderManager:

    def __init__(self):
        provider = os.getenv(
            "AI_PROVIDER", "groq"
        ).lower()

        if provider == "gemini":
            self.ai_client = GeminiClient()
        else:
            self.ai_client = GroqClient()

        self.normalizer = (
            ResponseNormalizer()
        )

        self.response_coordinator = (
            ResponseCoordinator()
        )

    def generate_ai_response(
            self,
            prompt: str
    ):
        raw_response = (
            self.ai_client
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

        coordinated_response = (
            self.response_coordinator
            .coordinate_response(
                normalized_response
            )
        )

        return coordinated_response