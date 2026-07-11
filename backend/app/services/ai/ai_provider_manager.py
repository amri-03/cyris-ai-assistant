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
        self.providers = []
        
        # Load Groq keys (Specialty: fast_chat, coding)
        for i in range(1, 4):
            key = os.getenv(f"GROQ_API_KEY_{i}")
            if key:
                self.providers.append({
                    "name": "groq",
                    "client": GroqClient(api_key=key),
                    "capabilities": ["fast_chat", "coding"]
                })
        # Backwards compatibility
        legacy_groq = os.getenv("GROQ_API_KEY")
        if legacy_groq and not any(p["client"].api_key == legacy_groq for p in self.providers):
            self.providers.append({
                "name": "groq",
                "client": GroqClient(api_key=legacy_groq),
                "capabilities": ["fast_chat", "coding"]
            })
            
        # Load Gemini keys (Specialty: complex_reasoning, general)
        for i in range(1, 4):
            key = os.getenv(f"GEMINI_API_KEY_{i}")
            if key:
                self.providers.append({
                    "name": "gemini",
                    "client": GeminiClient(api_key=key),
                    "capabilities": ["complex_reasoning", "general"]
                })
        legacy_gemini = os.getenv("GEMINI_API_KEY")
        if legacy_gemini and not any(p["client"].api_key == legacy_gemini for p in self.providers):
            self.providers.append({
                "name": "gemini",
                "client": GeminiClient(api_key=legacy_gemini),
                "capabilities": ["complex_reasoning", "general"]
            })

        self.normalizer = ResponseNormalizer()
        self.response_coordinator = ResponseCoordinator()
        self.response_cleaner = ResponseCleaner()
        self.ai_client = None

    def _route_providers(self, prompt: str) -> list:
        if not self.providers:
            return []
            
        # Determine primary capability based on prompt context
        prompt_lower = prompt.lower()
        if len(prompt) > 1000 or "analyze" in prompt_lower or "reason" in prompt_lower:
            primary_tag = "complex_reasoning"
        else:
            primary_tag = "fast_chat"
            
        # Sort providers: ones matching primary_tag first
        return sorted(
            self.providers, 
            key=lambda p: 0 if primary_tag in p["capabilities"] else 1
        )

    def generate_ai_response(
            self,
            prompt: str,
            add_to_history: bool = True
    ):
        ordered_providers = self._route_providers(prompt)
        if not ordered_providers:
            return "No AI providers configured. Please add API keys to .env"

        raw_response = None
        
        for provider_info in ordered_providers:
            client = provider_info["client"]
            self.ai_client = client # Set current active client for thread callbacks
            
            raw_response = client.generate_response(prompt, add_to_history=False)
            
            if isinstance(raw_response, dict) and raw_response.get("status") == "failure":
                print(f"Provider {provider_info['name']} failed. Attempting next provider...")
                continue
                
            break
            
        if isinstance(raw_response, dict) and raw_response.get("status") == "failure":
            return "Error: All configured AI providers failed. Please check your API keys and rate limits."

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