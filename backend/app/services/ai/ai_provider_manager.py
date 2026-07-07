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

from app.services.ai.response_cleaner import (
    ResponseCleaner
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

        self.response_cleaner = (
            ResponseCleaner()
        )

    def generate_ai_response(
            self,
            prompt: str,
            add_to_history: bool = True
    ):
        raw_response = (
            self.ai_client
            .generate_response(
                prompt,
                add_to_history=False
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

        if isinstance(coordinated_response, dict):

            final_response = (
                coordinated_response.get("response")
            )

            if isinstance(final_response, dict):
                final_response = (
                        final_response.get("response")
                        or final_response.get("content")
                        or str(final_response)
                )

        else:

            final_response = str(
                coordinated_response
            )

        cleaned_response = (
            self.response_cleaner
            .clean_response(
                final_response
            )
        )

        if add_to_history and normalized_response.get("status") != "failure":
            from app.memory.conversation_history_service import ConversationHistoryService
            from app.memory.continuity_memory_service import ContinuityMemoryService
            
            history_service = ConversationHistoryService()
            continuity_memory = ContinuityMemoryService()
            
            history_service.add_message("user", prompt)
            history_service.add_message("assistant", cleaned_response)
            
            import threading
            client_instance = getattr(self.ai_client, "client", None)
            thread = threading.Thread(
                target=continuity_memory.save_continuity,
                args=(client_instance, prompt)
            )
            thread.daemon = True
            thread.start()

        return cleaned_response