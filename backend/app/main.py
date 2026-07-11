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
        SET feedback = %s
        WHERE id = (
            SELECT id FROM messages
            WHERE role = 'assistant' AND content = %s
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
            "UPDATE user_continuity SET retired = 1, last_updated = %s WHERE identity = %s",
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

    # Look for the user's name in continuity items
    user_name = None
    for item in items:
        content = item.get("content", "")
        if "name is" in content.lower() or "call me" in content.lower():
            words = content.split()
            if "is" in words:
                idx = words.index("is")
                if idx + 1 < len(words):
                    user_name = words[idx + 1].strip('.')
            elif "me" in words:
                idx = words.index("me")
                if idx + 1 < len(words):
                    user_name = words[idx + 1].strip('.')
            if user_name:
                break
                
    if user_name:
        greeting = f"Hello {user_name}! How can I help you today?"
    else:
        greeting = "Hello! How can I help you today?"

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
            VALUES (%s, %s, %s, %s, %s, 0, %s, %s)
            ON CONFLICT (identity) DO NOTHING
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

@app.get("/goals")
def get_goals():
    from app.services.ai.productivity_service import ProductivityService
    service = ProductivityService()
    return {"goals": service.get_active_goals_with_tasks()}

class GoalRequest(BaseModel):
    title: str
    description: Optional[str] = ""

@app.post("/goals")
def create_goal(req: GoalRequest):
    from app.services.ai.productivity_service import ProductivityService
    service = ProductivityService()
    goal_id = service.create_goal(req.title, req.description)
    return {"status": "success", "goal_id": goal_id}

class TaskRequest(BaseModel):
    description: str

@app.post("/goals/{goal_id}/tasks")
def add_task(goal_id: int, req: TaskRequest):
    from app.services.ai.productivity_service import ProductivityService
    service = ProductivityService()
    task_id = service.add_task_to_goal(goal_id, req.description)
    return {"status": "success", "task_id": task_id}

@app.post("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    from app.services.ai.productivity_service import ProductivityService
    service = ProductivityService()
    service.complete_task(task_id)
    return {"status": "success"}
