import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute('DROP INDEX IF EXISTS message_embeddings_idx')
cursor.execute('ALTER TABLE message_embeddings ALTER COLUMN embedding TYPE vector(3072)')
conn.commit()
conn.close()
print('Table altered to 3072 dimensions')
