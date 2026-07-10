import os
from typing import List, Dict, Any
from google.generativeai import embed_content
from app.db import get_db_connection

class VectorMemoryService:
    def __init__(self):
        # We assume GOOGLE_API_KEY is loaded in environment
        self.model_name = "models/text-embedding-004"
    
    def generate_embedding(self, text: str) -> List[float]:
        try:
            result = embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []

    def store_message_embedding(self, message_id: int, content: str):
        embedding = self.generate_embedding(content)
        if not embedding:
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO message_embeddings (message_id, embedding, created_at)
                VALUES (%s, %s, datetime('now'))
            """, (message_id, embedding))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error storing embedding: {e}")

    def semantic_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self.generate_embedding(query)
        if not query_embedding:
            return []
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # <=>: cosine distance, <->: L2 distance, <#>: inner product
            # pgvector allows querying by cosine distance using <=>
            cursor.execute("""
                SELECT m.id, m.role, m.content, m.created_at, 
                       (me.embedding <=> %s::vector) as distance
                FROM message_embeddings me
                JOIN messages m ON me.message_id = m.id
                ORDER BY distance ASC
                LIMIT %s
            """, (query_embedding, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row['id'],
                    "role": row['role'],
                    "content": row['content'],
                    "created_at": row['created_at'],
                    "distance": row['distance']
                })
            
            cursor.close()
            conn.close()
            return results
        except Exception as e:
            print(f"Error during semantic search: {e}")
            return []
