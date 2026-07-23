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

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv(
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
            add_to_history: bool = True,
            session_id: str = None
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
                .get_messages(session_id)
            )

            # Recreate system instructions dynamically
            from app.services.ai.vector_memory_service import VectorMemoryService
            from app.services.ai.productivity_service import ProductivityService
            
            try:
                vm_service = VectorMemoryService()
                semantic_results = vm_service.semantic_search(prompt, limit=3, exclude_session_id=session_id)
                semantic_context = "\n".join([f"- {r['created_at']}: {r['content']}" for r in semantic_results]) if semantic_results else ""
            except Exception:
                semantic_context = ""

            try:
                prod_service = ProductivityService()
                goals = prod_service.get_active_goals_with_tasks()
                prod_context_lines = []
                for g in goals:
                    prod_context_lines.append(f"Goal: {g['title']} (Progress: {g['progress']}%)")
                    for t in g['tasks']:
                        status_str = "[x]" if t['is_completed'] else "[ ]"
                        prod_context_lines.append(f"  {status_str} {t['description']}")
                productivity_context = "\n".join(prod_context_lines)
            except Exception:
                productivity_context = ""

            system_prompt = self.system_prompt_manager.build_system_prompt(
                semantic_context=semantic_context, 
                productivity_context=productivity_context
            )
            mood_context = self.continuity_memory.build_mood_context()
            if mood_context:
                full_system_prompt += f"\n\n{mood_context}"

            if history:
                last_msg = history[-1]
                if last_msg.get("created_at"):
                    try:
                        from datetime import datetime
                        last_dt = datetime.fromisoformat(last_msg["created_at"])
                        now_dt = datetime.now()
                        if last_dt.date() < now_dt.date():
                            days_diff = (now_dt.date() - last_dt.date()).days
                            full_system_prompt += (
                                f"\n\n[Temporal Gap Note: The previous message in this session was sent {days_diff} day(s) ago on {last_dt.strftime('%A, %B %d, %Y')}. "
                                f"Be implicitly aware of this time gap so you do not assume yesterday's active discussion or unfinished task is occurring right now in real time. "
                                f"Do NOT explicitly announce or greet about the calendar day transition unless relevant to the user's prompt.]"
                            )
                    except Exception:
                        pass
            
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
