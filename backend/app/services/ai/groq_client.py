import os
from groq import Groq

from app.services.ai.system_prompt_manager import (
    SystemPromptManager
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

            mood_context = self.continuity_memory.build_mood_context()
            from app.services.ai.vector_memory_service import VectorMemoryService
            from app.services.ai.productivity_service import ProductivityService
            
            try:
                vm_service = VectorMemoryService()
                semantic_results = vm_service.semantic_search(prompt, limit=3)
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
            
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "system",
                    "content": f"Important continuity context:\n{memory_context}"
                }
            ]
            if mood_context:
                messages.append({
                    "role": "system",
                    "content": mood_context
                })

            from datetime import datetime
            for msg in history:
                time_prefix = ""
                if msg.get("created_at"):
                    try:
                        dt = datetime.fromisoformat(msg["created_at"])
                        time_prefix = dt.strftime("[%Y-%m-%d %H:%M] ")
                    except Exception:
                        pass
                
                content_text = msg["content"]
                if msg["role"] == "assistant" and msg.get("feedback"):
                    content_text = f"{content_text}\n\n[User Feedback: {msg['feedback'].upper()}]"
                
                messages.append({
                    "role": msg["role"],
                    "content": f"{time_prefix}{content_text}"
                })

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

            return response

        except Exception as error:
            return {
                "status": "failure",
                "error": str(error)
            }