import os
import cohere

from app.services.ai.system_prompt_manager import SystemPromptManager
from app.memory.continuity_memory_service import ContinuityMemoryService
from app.memory.conversation_history_service import ConversationHistoryService

class CohereClient:

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")

        self.system_prompt_manager = SystemPromptManager()
        self.continuity_memory = ContinuityMemoryService()
        self.history_service = ConversationHistoryService()

        self.client = None

        if self.api_key:
            self.client = cohere.ClientV2(api_key=self.api_key)

    def generate_response(self, prompt: str, add_to_history: bool = True, session_id: str = None):
        if not self.api_key or not self.client:
            return {
                "status": "failure",
                "error": "COHERE_API_KEY not configured."
            }

        try:
            memory_context = self.continuity_memory.build_priority_briefing()
            history = self.history_service.get_messages(session_id)

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
            full_system_prompt = f"{system_prompt}\n\nImportant continuity context:\n{memory_context}"
            if mood_context:
                full_system_prompt += f"\n\n{mood_context}"

            messages = [
                {
                    "role": "system",
                    "content": full_system_prompt
                }
            ]

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
                    "role": "assistant" if msg["role"] == "assistant" else "user",
                    "content": f"{time_prefix}{content_text}"
                })

            messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            # Use command-r as the default conversational model
            response = self.client.chat(
                model="command-r-plus-08-2024",
                messages=messages
            )

            # Inject .text property so it acts somewhat uniformly
            if hasattr(response, 'message') and hasattr(response.message, 'content'):
                response.text = response.message.content[0].text
                
            return response

        except Exception as error:
            return {
                "status": "failure",
                "error": str(error)
            }
