import sqlite3
from datetime import datetime
from app.db import get_db_connection

class ConversationHistoryService:

    def add_message(
            self,
            role: str,
            content: str
    ):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        timestamp_str = datetime.now().isoformat()
        
        # Insert new message
        cursor.execute(
            "INSERT INTO messages (role, content, created_at, session_active) VALUES (?, ?, ?, 1)",
            (role, content, timestamp_str)
        )
        
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

    def get_messages(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content, created_at FROM messages WHERE session_active = 1 ORDER BY id ASC"
        )
        rows = cursor.fetchall()
        
        conn.close()
        
        return [
            {
                "role": row["role"],
                "content": row["content"],
                "created_at": row["created_at"]
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