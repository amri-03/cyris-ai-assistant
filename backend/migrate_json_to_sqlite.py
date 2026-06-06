import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

def run_migration():
    db_path = Path("data/cyris.db")
    history_json_path = Path("data/conversation_memory.json")
    continuity_json_path = Path("data/user_continuity.json")
    
    print("Starting JSON to SQLite migration...")
    
    # Ensure database is initialized
    from app.db import init_db, get_db_connection
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Migrate Conversation Memory
    if history_json_path.exists():
        try:
            with open(history_json_path, "r", encoding="utf-8") as f:
                history_data = json.load(f)
                
            messages = history_data.get("messages", [])
            print(f"Found {len(messages)} messages in conversation_memory.json")
            
            # Check if messages table is empty
            cursor.execute("SELECT COUNT(*) FROM messages")
            count = cursor.fetchone()[0]
            
            if count == 0:
                base_time = datetime.now() - timedelta(days=14)  # Spread them over 14 days
                for i, msg in enumerate(messages):
                    role = msg.get("role")
                    content = msg.get("content")
                    # Approximate a progressive timestamp to keep chronological order
                    msg_time = (base_time + timedelta(seconds=i * 60)).isoformat()
                    
                    cursor.execute(
                        "INSERT INTO messages (role, content, created_at, session_active) VALUES (?, ?, ?, 0)",
                        (role, content, msg_time)
                    )
                # Mark the last 10 messages as active for the current session
                cursor.execute("""
                    UPDATE messages 
                    SET session_active = 1 
                    WHERE id IN (
                        SELECT id FROM messages 
                        ORDER BY id DESC 
                        LIMIT 10
                    )
                """)
                print(f"Successfully migrated {len(messages)} messages to SQLite.")
            else:
                print("Messages table already contains data. Skipping message migration.")
        except Exception as e:
            print(f"Error migrating messages: {e}")
    else:
        print("conversation_memory.json not found. Skipping message migration.")
        
    # 2. Migrate User Continuity (Long-Term Memory)
    if continuity_json_path.exists():
        try:
            with open(continuity_json_path, "r", encoding="utf-8") as f:
                continuity_data = json.load(f)
                
            items = continuity_data.get("continuity_items", [])
            print(f"Found {len(items)} continuity items in user_continuity.json")
            
            # Migrate items
            for item in items:
                identity = item.get("identity")
                item_type = item.get("type")
                content = item.get("content")
                importance = item.get("importance", "medium")
                priority = item.get("priority", 3)
                created_at = item.get("created_at") or datetime.now().isoformat()
                last_updated = item.get("last_updated") or datetime.now().isoformat()
                retired = 1 if item.get("retired") else 0
                
                # Check if item exists in DB
                cursor.execute("SELECT COUNT(*) FROM user_continuity WHERE identity = ?", (identity,))
                exists = cursor.fetchone()[0]
                
                if not exists:
                    cursor.execute("""
                        INSERT INTO user_continuity (identity, type, content, importance, priority, retired, created_at, last_updated)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (identity, item_type, content, importance, priority, retired, created_at, last_updated))
            
            print("Successfully migrated user continuity items to SQLite.")
        except Exception as e:
            print(f"Error migrating continuity items: {e}")
    else:
        print("user_continuity.json not found. Skipping continuity migration.")
        
    conn.commit()
    conn.close()
    print("Migration finished.")

if __name__ == "__main__":
    run_migration()
