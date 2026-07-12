import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db import get_db_connection

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM messages LIMIT 1")
    msg_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO message_embeddings (message_id, embedding, created_at) VALUES (%s, %s, 'test')", (msg_id, [0.1]*3072,))
    conn.rollback()
    print('SUCCESSFULLY inserted 3072 vector!')
except Exception as e:
    print(f"FAILED: {e}")
