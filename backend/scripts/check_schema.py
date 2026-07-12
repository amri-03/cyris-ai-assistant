import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT atttypmod FROM pg_attribute WHERE attrelid = 'message_embeddings'::regclass AND attname = 'embedding'")
print("Columns in message_embeddings:")
for row in cursor.fetchall():
    print(row)
conn.close()
