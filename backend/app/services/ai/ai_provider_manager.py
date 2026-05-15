from app.services.ai.openai_client import (
    OpenAIClient
)

from app.services.ai.response_normalizer import (
    ResponseNormalizer
)

from app.services.ai.response_coordinator import (
    ResponseCoordinator
)


class AIProviderManager:

    def __init__(self):
        self.openai_client = (
            OpenAIClient()
        )

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

        coordinated_response = (
            self.response_coordinator
            .coordinate_response(
                normalized_response
            )
        )

        return coordinated_response