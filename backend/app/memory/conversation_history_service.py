import sqlite3
from datetime import datetime
from app.db import get_db_connection

class ConversationHistoryService:

    def add_message(
            self,
            role: str,
            content: str,
            session_id: str = None
    ):
        # Clean assistant messages before database insertion to prevent thinking trace leaks
        if role == "assistant":
            try:
                from app.services.ai.response_cleaner import ResponseCleaner
                content = ResponseCleaner().clean_response(content)
            except Exception:
                # Fallback to saving original content if cleaner fails
                pass

        conn = get_db_connection()
        cursor = conn.cursor()
        
        timestamp_str = datetime.now().isoformat()
        
        # Insert new message
        cursor.execute(
            "INSERT INTO messages (session_id, role, content, created_at, session_active) VALUES (%s, %s, %s, %s, 1) RETURNING id",
            (session_id, role, content, timestamp_str)
        )
        message_id = cursor.fetchone()[0]
        
        # Enforce sliding window of 10 messages for active session
        cursor.execute("""
            UPDATE messages 
            SET session_active = 0 
            WHERE id NOT IN (
                SELECT id FROM messages 
                WHERE session_active = 1 
                ORDER BY id DESC 
                LIMIT 10
            ) AND session_active = 1
        """)
        
        conn.commit()
        conn.close()
        
        # Save vector embedding asynchronously
        try:
            import threading
            from app.services.ai.vector_memory_service import VectorMemoryService
            vm_service = VectorMemoryService()
            thread = threading.Thread(
                target=vm_service.store_message_embedding,
                args=(message_id, content)
            )
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Error starting vector memory thread: {e}")

    def get_messages(self, session_id: str = None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if session_id:
            cursor.execute(
                """
                SELECT role, content, created_at, feedback 
                FROM (
                    SELECT * FROM messages 
                    WHERE session_id = %s 
                    ORDER BY id DESC 
                    LIMIT 10
                ) sub
                ORDER BY id ASC
                """,
                (session_id,)
            )
        else:
            cursor.execute(
                "SELECT role, content, created_at, feedback FROM messages WHERE session_active = 1 ORDER BY id ASC"
            )
        
        rows = cursor.fetchall()
        
        conn.close()
        
        return [
            {
                "role": row["role"],
                "content": row["content"],
                "created_at": row["created_at"],
                "feedback": row["feedback"]
            }
            for row in rows
        ]

    def save_history(self, history):
        # Kept for backward compatibility, translates to saving a list of messages
        # Usually used for clearing or bulk deactivating
        if "messages" in history and not history["messages"]:
            self.clear_history()

    def clear_history(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Deactivate all active messages instead of deleting them to preserve history
        cursor.execute("UPDATE messages SET session_active = 0 WHERE session_active = 1")
        
        conn.commit()
        conn.close()