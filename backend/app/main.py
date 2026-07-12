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
    session_id: Optional[str] = None


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


@app.get("/sessions")
def get_sessions():
    from app.services.session_service import SessionService
    return {"sessions": SessionService.get_all_sessions()}

@app.post("/sessions")
def create_session():
    from app.services.session_service import SessionService
    return SessionService.create_session()

@app.get("/sessions/{session_id}/messages")
def get_session_messages(session_id: str):
    from app.services.session_service import SessionService
    return {"messages": SessionService.get_session_messages(session_id)}

@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    from app.services.session_service import SessionService
    SessionService.delete_session(session_id)
    return {"status": "success"}

@app.post("/chat")
def chat(request: PromptRequest):
    session_id = request.session_id
    from app.db import get_db_connection
    from datetime import datetime
    import threading
    from app.services.session_service import SessionService
    
    is_first_message = False
    
    if not session_id:
        session = SessionService.create_session()
        session_id = session["id"]
        is_first_message = True
    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM messages WHERE session_id = %s", (session_id,))
        is_first_message = cur.fetchone()[0] == 0
        now = datetime.now().isoformat()
        cur.execute("UPDATE sessions SET updated_at = %s WHERE id = %s", (now, session_id))
        conn.commit()
        conn.close()

    ai_response = (
        ai_provider.generate_ai_response(
            request.prompt,
            session_id=session_id
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

    # Trigger real-time shadow backup
    from app.services.backup_service import BackupService
    thread = threading.Thread(target=BackupService().backup_to_json)
    thread.daemon = True
    thread.start()
    
    if is_first_message:
        def generate_title():
            try:
                title_prompt = f"Generate a short title (max 5 words) for this conversation based on the user's first message: '{request.prompt}'. Do not use quotes or prefixes."
                title_response = ai_provider.generate_ai_response(title_prompt, add_to_history=False)
                if isinstance(title_response, dict):
                    title = title_response.get("response") or title_response.get("content") or str(title_response)
                else:
                    title = str(title_response)
                
                title = title.replace('"', '').replace("'", "").strip()
                if title:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("UPDATE sessions SET title = %s WHERE id = %s", (title, session_id))
                    conn.commit()
                    conn.close()
            except Exception as e:
                print(f"Error generating title: {e}")
                
        t = threading.Thread(target=generate_title)
        t.daemon = True
        t.start()

    return {
        "response": str(content),
        "session_id": session_id
    }


@app.get("/session-start", deprecated=True)
def session_start():
    # Deprecated: Frontend should create a new session via POST /sessions or POST /chat directly
    return {"message": "Hello! How can I help you today?"}

@app.post("/session/conclude", deprecated=True)
def conclude_session():
    # Deprecated
    return {"status": "success", "summary": "Session concluded."}




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


@app.get("/session-messages", deprecated=True)
def session_messages():
    return {"messages": []}

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
