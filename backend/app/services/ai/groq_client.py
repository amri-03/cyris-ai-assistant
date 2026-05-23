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

        self.client = None

        if self.api_key:
            self.client = Groq(
                api_key=self.api_key
            )

    def generate_response(
            self,
            prompt: str,
            model="llama-3.3-70b-versatile"
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
                            "role": "system",
                            "content": (
                                "Previous conversation context:\n"
                                f"{memory_context}"
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
            )

            content = (
                response
                .choices[0]
                .message
                .content
            )

            self.memory_service.save_message(
                "user",
                prompt
            )

            self.continuity_memory.save_continuity(
                self.client,
                prompt
            )

            self.memory_service.save_message(
                "assistant",
                content
            )

            return response

        except Exception as error:
            return {
                "status": "failure",
                "error": str(error)
            }