import sys, os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db, get_db_connection
import time
import json

client = TestClient(app)

def test_backup_restore():
    print("1. Sending message to trigger backup...")
    response = client.post("/chat", json={"prompt": "Hello Cyris, this is a test of the ironclad backup system."})
    print(f"Chat Response: {response.json()}")
    
    # Wait for background thread to write backup
    time.sleep(2)
    
    backup_file = Path(__file__).resolve().parent.parent / "data" / "database_backup.json"
    if backup_file.exists():
        with open(backup_file, "r") as f:
            data = json.load(f)
            msg_count = len(data.get("messages", []))
            print(f"2. Backup verified! Contains {msg_count} messages.")
    else:
        print("2. FAILED: Backup file not found!")
        return
        
    print("3. Wiping Postgres to simulate catastrophic failure...")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE message_embeddings CASCADE")
    cursor.execute("TRUNCATE TABLE messages RESTART IDENTITY CASCADE")
    cursor.execute("TRUNCATE TABLE sessions CASCADE")
    cursor.execute("TRUNCATE TABLE user_continuity CASCADE")
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM messages")
    print(f"Messages in DB after wipe: {cursor.fetchone()[0]}")
    conn.close()
    
    print("4. Triggering system startup (init_db) to test auto-healing...")
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM messages")
    restored_count = cursor.fetchone()[0]
    print(f"5. Messages in DB after auto-restore: {restored_count}")
    
    if restored_count == msg_count:
        print("SUCCESS! Ironclad backup and restore is fully functional.")
    else:
        print("FAILED: Message counts do not match.")

if __name__ == "__main__":
    test_backup_restore()
