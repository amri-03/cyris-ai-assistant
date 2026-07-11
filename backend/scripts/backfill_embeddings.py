import sys
import os
import time
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app.db import get_db_connection
from app.services.ai.vector_memory_service import VectorMemoryService

def backfill():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, content FROM messages 
        WHERE id NOT IN (SELECT message_id FROM message_embeddings)
    """)
    rows = cursor.fetchall()
    
    vm_service = VectorMemoryService()
    
    print(f"Found {len(rows)} messages without embeddings. Backfilling...")
    
    for row in rows:
        msg_id = row['id']
        content = row['content']
        try:
            vm_service.store_message_embedding(msg_id, content)
            print(f"Stored embedding for message {msg_id}")
            time.sleep(1) # Sleep to avoid rate limits
        except Exception as e:
            print(f"Error for {msg_id}: {e}")
            
    conn.close()
    print("Backfill Complete!")

if __name__ == "__main__":
    backfill()
