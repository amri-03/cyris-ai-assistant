import json
import sys
import os
import time
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app.db import get_db_connection
from app.services.ai.vector_memory_service import VectorMemoryService

def migrate():
    history_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'runtime_history.json')
    if not os.path.exists(history_file):
        print("No runtime_history.json found.")
        return
        
    with open(history_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    messages = data if isinstance(data, list) else data.get("messages", [])
    if not messages:
        print("No messages found in runtime_history.json.")
        return
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    vm = VectorMemoryService()
    
    print(f"Found {len(messages)} legacy messages. Migrating to PostgreSQL...")
    
    # We will spread them chronologically before the oldest message currently in postgres
    # The oldest in postgres right now is '2026-06-29T14:30:03.938554'
    cursor.execute("SELECT created_at FROM messages ORDER BY id ASC LIMIT 1")
    row = cursor.fetchone()
    if row:
        base_time_str = row[0]
        base_time = datetime.fromisoformat(base_time_str) - timedelta(days=60)
    else:
        base_time = datetime.now() - timedelta(days=60)
        
    inserted_count = 0
    for i, msg in enumerate(messages):
        role = msg.get("role")
        content = msg.get("content")
        if not content: continue
        
        msg_time = (base_time + timedelta(hours=i)).isoformat()
        
        # Insert into messages
        cursor.execute("""
            INSERT INTO messages (role, content, created_at, session_active)
            VALUES (%s, %s, %s, 0) RETURNING id
        """, (role, content, msg_time))
        msg_id = cursor.fetchone()[0]
        
        # Store embedding
        try:
            vm.store_message_embedding(msg_id, content)
            inserted_count += 1
            if inserted_count % 10 == 0:
                print(f"Migrated and embedded {inserted_count} messages...")
                conn.commit()
            time.sleep(0.5) # Avoid rate limits
        except Exception as e:
            print(f"Error generating embedding for legacy message {msg_id}: {e}")
            
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Successfully migrated {inserted_count} legacy messages!")

if __name__ == '__main__':
    migrate()
