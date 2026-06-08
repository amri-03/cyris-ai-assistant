import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.ai.ai_provider_manager import AIProviderManager
from app.memory.continuity_memory_service import ContinuityMemoryService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.db import init_db
init_db()

ai_provider = AIProviderManager()
continuity_memory = ContinuityMemoryService()


@app.get("/")
def root():
    return {"message": "Cyris AI Assistant backend is running"}


class PromptRequest(BaseModel):
    prompt: str


class FeedbackRequest(BaseModel):
    content: str
    feedback: Optional[str] = None


@app.post("/message/feedback")
def save_feedback(request: FeedbackRequest):
    from app.db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update the feedback column for the most recent message with matching content and role = 'assistant'
    cursor.execute("""
        UPDATE messages
        SET feedback = ?
        WHERE id = (
            SELECT id FROM messages
            WHERE role = 'assistant' AND content = ?
            ORDER BY id DESC
            LIMIT 1
        )
    """, (request.feedback, request.content))
    
    conn.commit()
    conn.close()
    
    return {"status": "success"}


@app.post("/chat")
def chat(request: PromptRequest):
    ai_response = (
        ai_provider.generate_ai_response(
            request.prompt
        )
    )

    if isinstance(ai_response, dict):

        content = (
                ai_response.get("response")
                or ai_response.get("content")
        )

        if isinstance(content, dict):
            content = (
                    content.get("response")
                    or content.get("content")
            )

    else:

        content = ai_response

    return {
        "response": str(content),
        "session_id": "default-session"
    }


@app.get("/session-start")
def session_start():
    from app.memory.conversation_history_service import ConversationHistoryService
    history_service = ConversationHistoryService()

    continuity = (
        continuity_memory
        .load_memory()
    )

    items = [item for item in continuity.get("continuity_items", []) if not item.get("retired", False)]

    if not items:
        default_greeting = (
            "Hello. I'm Cyris. "
            "Tell me a little about yourself "
            "and what matters to you right now."
        )
        history_service.save_history({"messages": []})
        history_service.add_message("assistant", default_greeting)
        return {
            "message": default_greeting
        }

    # Generate a dynamic greeting using the active AI provider based on continuity context
    formatted_items = []
    for item in items:
        formatted_items.append(f"- {item.get('content')} ({item.get('type')})")
    items_str = "\n".join(formatted_items)

    prompt = f"""
    You are Cyris, a calm, intelligent, and context-aware AI assistant.
    The user is starting a new session. Generate a brief, warm, and natural welcome-back greeting.
    Reference 1 or 2 of their active continuity areas naturally so they feel you remember them, but keep it calm, light, and concise (1-2 sentences). Do not use robotic phrasing like "Welcome back! I see you are..." or be overly enthusiastic.
    
    CRITICAL: Strictly output ONLY the greeting text itself. Do not include any reasoning, chain-of-thought, self-corrections, planning, or headers in your output.
    
    Active continuity profile:
    {items_str}
    
    Greeting:
    """

    try:
        response = ai_provider.generate_ai_response(prompt, add_to_history=False)
        if isinstance(response, dict):
            greeting = response.get("response") or response.get("content") or str(response)
            if isinstance(greeting, dict):
                greeting = greeting.get("response") or greeting.get("content") or str(greeting)
        else:
            greeting = str(response)

        greeting = greeting.strip().strip('"').strip("'")
    except Exception:
        # Fallback to template if LLM call fails
        latest = items[-1]
        content = latest.get("content", "something important")
        greeting = f"Welcome back. Last time we were discussing {content}. Would you like to continue from there?"

    # Reset history for the new session and append the greeting
    history_service.save_history({"messages": []})
    history_service.add_message("assistant", greeting)

    return {
        "message": greeting
    }



@app.get("/memory-status")
def memory_status():
    memory = (
        continuity_memory
        .load_memory()
    )

    return {
        "continuity_items":
            memory.get(
                "continuity_items",
                []
            )
    }


@app.delete("/memory/{identity}")
def delete_memory_item(identity: str):
    success = continuity_memory.delete_continuity_item(identity)
    if success:
        return {"status": "success", "message": f"Memory item '{identity}' deleted."}
    else:
        return {"status": "error", "message": "Failed to delete memory item."}


@app.post("/memory/reconcile")
def reconcile_memory():
    try:
        from app.memory.memory_reconciler import MemoryReconciler
        reconciler = MemoryReconciler()
        result = reconciler.rebuild_memory_from_history(ai_provider)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/session-messages")
def session_messages():
    from app.memory.conversation_history_service import ConversationHistoryService
    history_service = ConversationHistoryService()
    messages = history_service.get_messages()
    return {"messages": messages}



