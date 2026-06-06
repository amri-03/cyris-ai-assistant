import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")
import google.generativeai as genai

from app.services.ai.system_prompt_manager import (
    SystemPromptManager
)

from app.services.memory.conversation_memory_service import (
    ConversationMemoryService
)

from app.memory.continuity_memory_service import (
    ContinuityMemoryService
)

from app.memory.conversation_history_service import (
    ConversationHistoryService
)


class GeminiClient:

    def __init__(self):
        self.api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        self.system_prompt_manager = (
            SystemPromptManager()
        )

        self.memory_service = (
            ConversationMemoryService()
        )

        self.continuity_memory = (
            ContinuityMemoryService()
        )

        self.history_service = (
            ConversationHistoryService()
        )

        self.model = None

        if self.api_key:
            genai.configure(api_key=self.api_key)

    def generate_response(
            self,
            prompt: str,
            add_to_history: bool = True
    ):
        if not self.api_key:
            return {
                "status": "failure",
                "error": (
                    "GEMINI_API_KEY not configured."
                )
            }

        try:
            # Build memory and history context
            memory_context = (
                self.continuity_memory
                .build_priority_briefing()
            )

            history = (
                self.history_service
                .get_messages()
            )

            # Recreate GenerativeModel with system instructions dynamically
            system_prompt = self.system_prompt_manager.build_system_prompt()
            full_system_prompt = f"{system_prompt}\n\nImportant continuity context:\n{memory_context}"
            
            model_name = os.getenv("GEMINI_MODEL", "gemma-4-26b-a4b-it")
            model = genai.GenerativeModel(
                model_name,
                system_instruction=full_system_prompt
            )

            # Map history to Gemini format (user/model roles)
            gemini_history = []
            for msg in history:
                role = "model" if msg["role"] == "assistant" else "user"
                gemini_history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })

            # Append current user prompt
            gemini_history.append({
                "role": "user",
                "parts": [prompt]
            })

            # Generate response
            response = model.generate_content(
                contents=gemini_history
            )

            content = response.text

            from app.services.ai.response_cleaner import ResponseCleaner
            cleaned_content = ResponseCleaner().clean_response(content)

            if add_to_history:
                # Update history and memory services
                self.history_service.add_message(
                    "user",
                    prompt
                )

                self.history_service.add_message(
                    "assistant",
                    cleaned_content
                )

                self.memory_service.save_message(
                    "user",
                    prompt
                )

                # Run memory extraction in a background thread to avoid blocking the main chat response
                import threading
                thread = threading.Thread(
                    target=self.continuity_memory.save_continuity,
                    args=(None, prompt)
                )
                thread.daemon = True
                thread.start()

                self.memory_service.save_message(
                    "assistant",
                    cleaned_content
                )

            return response

        except Exception as error:
            return {
                "status": "failure",
                "error": str(error)
            }