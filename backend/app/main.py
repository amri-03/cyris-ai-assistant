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
    from datetime import datetime
    from app.memory.conversation_history_service import ConversationHistoryService
    history_service = ConversationHistoryService()

    continuity = (
        continuity_memory
        .load_memory()
    )

    items = [item for item in continuity.get("continuity_items", []) if not item.get("retired", False)]

    # 1. Calculate time gap since last session
    from app.db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT created_at FROM messages ORDER BY id DESC LIMIT 1")
    last_msg_row = cursor.fetchone()
    
    gap_days = 0
    if last_msg_row:
        try:
            last_time = datetime.fromisoformat(last_msg_row["created_at"])
            delta = datetime.now() - last_time
            gap_days = delta.days
        except Exception:
            pass

    # 2. Retrieve and consume any active next_session_context
    cursor.execute(
        "SELECT identity, content FROM user_continuity WHERE type = 'session_context' AND retired = 0"
    )
    context_rows = cursor.fetchall()
    
    session_contexts = []
    timestamp_str = datetime.now().isoformat()
    for row in context_rows:
        session_contexts.append(row["content"])
        cursor.execute(
            "UPDATE user_continuity SET retired = 1, last_updated = ? WHERE identity = ?",
            (timestamp_str, row["identity"])
        )
    conn.commit()

    # 3. Scan for stale goals/projects/focus areas (last updated > 7 days ago)
    cursor.execute("""
        SELECT content, type, last_updated 
        FROM user_continuity 
        WHERE retired = 0 AND type IN ('goal', 'focus_area', 'project')
    """)
    continuity_rows = cursor.fetchall()
    
    stale_items = []
    now = datetime.now()
    for row in continuity_rows:
        try:
            last_updated = datetime.fromisoformat(row["last_updated"])
            delta = now - last_updated
            if delta.days >= 7:
                stale_items.append(f"- {row['content']} ({row['type']})")
        except Exception:
            pass
            
    conn.close()

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

    formatted_items = []
    for item in items:
        formatted_items.append(f"- {item.get('content')} ({item.get('type')})")
    items_str = "\n".join(formatted_items)

    # Get recent mood context for the greeting
    mood_context_str = continuity_memory.build_mood_context()
    mood_instruction = ""
    if mood_context_str:
        mood_instruction = f"""
The following is behavioral context from recent sessions. Use it to subtly adapt your greeting tone — do NOT mention mood detection or analysis to the user. Just naturally adjust warmth and energy:
{mood_context_str}
"""

    # Build gap and stale instructions
    gap_instruction = ""
    if gap_days > 0:
        gap_instruction += f"\nIt has been {gap_days} days since the user's last session. Subtly acknowledge the gap if it is long (e.g. 3+ days) without being dramatic."
        
    if session_contexts:
        contexts_str = "\n".join([f"- {c}" for c in session_contexts])
        gap_instruction += f"\nHere is context/reflection from the end of their last session. Reference these commitments or progress naturally:\n{contexts_str}"
        
    if stale_items:
        stale_str = "\n".join(stale_items)
        gap_instruction += f"\nThese active goals/projects haven't been discussed in over a week. If appropriate, gently ask the user for an update on one of them:\n{stale_str}"

    prompt = f"""
    You are Cyris, a calm, intelligent, and context-aware AI assistant.
    The user is starting a new session. Generate a brief, warm, and natural welcome-back greeting.
    Reference 1 or 2 of their active continuity areas naturally so they feel you remember them, but keep it calm, light, and concise (1-2 sentences). Do not use robotic phrasing like "Welcome back! I see you are..." or be overly enthusiastic.
    {mood_instruction}
    {gap_instruction}
    
    CRITICAL: Wrap any internal reasoning, thoughts, or planning inside a <thinking>...</thinking> block before your final response. The user-facing response must start immediately after the </thinking> tag and contain ONLY the greeting text itself.
    
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

        greeting = greeting.strip()
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


@app.post("/session/conclude")
def conclude_session():
    from datetime import datetime
    from app.memory.conversation_history_service import ConversationHistoryService
    history_service = ConversationHistoryService()
    messages = history_service.get_messages()

    if not messages or len(messages) <= 1:
        # If there's no chat, or only the start greeting, just clear and return
        history_service.clear_history()
        return {"status": "success", "summary": "Session concluded with no active conversation."}

    # Format history for summarization
    formatted_chat = []
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        formatted_chat.append(f"{role}: {msg['content']}")
    chat_history_str = "\n".join(formatted_chat)

    prompt = f"""
    You are Cyris, a supportive and context-aware assistant.
    The user is ending their current session. Summarize the session and extract key commitments/next steps.
    Format your response in a supportive, concise, and calm manner (maximum 3 bullet points, keep sentences very short and direct).
    Focus strictly on:
    - What was discussed/accomplished.
    - Commitments or next steps the user planned.
    
    CRITICAL: Wrap any internal reasoning, thoughts, or planning inside a <thinking>...</thinking> block before your final response. The user-facing summary text must start immediately after the </thinking> tag.
    
    Session Chat History:
    {chat_history_str}
    
    Summary:
    """

    try:
        response = ai_provider.generate_ai_response(prompt, add_to_history=False)
        if isinstance(response, dict):
            summary = response.get("response") or response.get("content") or str(response)
            if isinstance(summary, dict):
                summary = summary.get("response") or summary.get("content") or str(summary)
        else:
            summary = str(response)
        summary = summary.strip()
    except Exception:
        summary = "Session concluded. Let's resume progress next time."

    # Save to user_continuity table
    try:
        from app.db import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        timestamp_str = datetime.now().isoformat()
        identity = f"session_context_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        cursor.execute("""
            INSERT INTO user_continuity (identity, type, content, importance, priority, retired, created_at, last_updated)
            VALUES (?, ?, ?, ?, ?, 0, ?, ?)
        """, (identity, "session_context", summary, "high", 5, timestamp_str, timestamp_str))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to save session context: {e}")

    # Set active session messages to inactive
    history_service.clear_history()

    return {
        "status": "success",
        "summary": summary
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
    
    if messages:
        try:
            from datetime import datetime
            # Check if the last message is from a different calendar day
            last_msg_time = datetime.fromisoformat(messages[-1]["created_at"])
            if last_msg_time.date() != datetime.now().date():
                history_service.clear_history()
                messages = []
        except Exception as e:
            print(f"Error checking session messages date: {e}")
            
    return {"messages": messages}




