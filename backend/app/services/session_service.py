import uuid
from datetime import datetime
from app.db import get_db_connection

class SessionService:
    @staticmethod
    def get_all_sessions():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, created_at, updated_at FROM sessions ORDER BY updated_at DESC")
        sessions = [dict(row) for row in cur.fetchall()]
        conn.close()
        return sessions

    @staticmethod
    def create_session():
        conn = get_db_connection()
        cur = conn.cursor()
        session_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        cur.execute("INSERT INTO sessions (id, title, created_at, updated_at) VALUES (%s, %s, %s, %s)", 
                    (session_id, "New Chat", now, now))
        conn.commit()
        
        cur.execute("SELECT id, title, created_at, updated_at FROM sessions WHERE id = %s", (session_id,))
        session = dict(cur.fetchone())
        conn.close()
        return session
        
    @staticmethod
    def get_session_messages(session_id: str):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, role, content, created_at, feedback FROM messages WHERE session_id = %s ORDER BY id ASC", (session_id,))
        messages = [dict(row) for row in cur.fetchall()]
        conn.close()
        return messages

    @staticmethod
    def delete_session(session_id: str):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
        conn.commit()
        conn.close()
