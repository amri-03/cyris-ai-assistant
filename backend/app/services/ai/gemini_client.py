import os
from google import genai
from google.genai import types

from app.services.ai.system_prompt_manager import (
    SystemPromptManager
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

        self.continuity_memory = (
            ContinuityMemoryService()
        )

        self.history_service = (
            ConversationHistoryService()
        )

        self.client = None

        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def generate_response(
            self,
            prompt: str,
            add_to_history: bool = True
    ):
        if not self.api_key or not self.client:
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

            # Recreate system instructions dynamically
            system_prompt = self.system_prompt_manager.build_system_prompt()
            mood_context = self.continuity_memory.build_mood_context()
            full_system_prompt = f"{system_prompt}\n\nImportant continuity context:\n{memory_context}"
            if mood_context:
                full_system_prompt += f"\n\n{mood_context}"
            
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

            # Map history to Gemini format (user/model roles)
            from datetime import datetime
            gemini_history = []
            for msg in history:
                role = "model" if msg["role"] == "assistant" else "user"
                time_prefix = ""
                if msg.get("created_at"):
                    try:
                        dt = datetime.fromisoformat(msg["created_at"])
                        time_prefix = dt.strftime("[%Y-%m-%d %H:%M] ")
                    except Exception:
                        pass
                
                content_text = msg["content"]
                if role == "model" and msg.get("feedback"):
                    content_text = f"{content_text}\n\n[User Feedback: {msg['feedback'].upper()}]"
                
                gemini_history.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=f"{time_prefix}{content_text}")]
                    )
                )

            # Generate response using chat
            chat = self.client.chats.create(
                model=model_name,
                history=gemini_history,
                config=types.GenerateContentConfig(
                    system_instruction=full_system_prompt
                )
            )
            response = chat.send_message(prompt)
            content = response.text

            return response

        except Exception as error:
            return {
                "status": "failure",
                "error": str(error)
            }
