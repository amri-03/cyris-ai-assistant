import os
from groq import Groq

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


class GroqClient:

    def __init__(self):
        self.api_key = os.getenv(
            "GROQ_API_KEY"
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

        self.client = None

        if self.api_key:
            self.client = Groq(
                api_key=self.api_key
            )

    def generate_response(
            self,
            prompt: str,
            model="llama-3.3-70b-versatile",
            add_to_history: bool = True
    ):
        if not self.client:
            return {
                "status": "failure",
                "error": (
                    "GROQ_API_KEY not configured."
                )
            }

        try:
            memory_context = (
                self.continuity_memory
                .build_priority_briefing()
            )

            history = (
                self.history_service
                .get_messages()
            )

            messages = [
                {
                    "role": "system",
                    "content": (
                        self.system_prompt_manager
                        .build_system_prompt()
                    )
                },
                {
                    "role": "system",
                    "content": (
                        "Important continuity context:\n"
                        f"{memory_context}"
                    )
                }
            ]

            messages.extend(history)

            messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            response = (
                self.client.chat.completions.create(
                    model=model,
                    messages=messages
                )
            )

            content = (
                response
                .choices[0]
                .message
                .content
            )

            from app.services.ai.response_cleaner import ResponseCleaner
            cleaned_content = ResponseCleaner().clean_response(content)

            if add_to_history:
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
                    args=(self.client, prompt)
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