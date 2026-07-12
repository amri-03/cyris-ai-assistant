import os
from typing import List, Dict, Any
from google import genai
from google.genai import types
from app.db import get_db_connection

class VectorMemoryService:
    def __init__(self):
        self.model_name = "models/gemini-embedding-2"
        self.api_keys = []
        for i in range(1, 4):
            k = os.getenv(f"GEMINI_API_KEY_{i}")
            if k: self.api_keys.append(k)
        legacy_key = os.getenv("GEMINI_API_KEY")
        if legacy_key and legacy_key not in self.api_keys:
            self.api_keys.append(legacy_key)
            
        self.current_key_idx = 0
    
    def generate_embedding(self, text: str) -> List[float]:
        if not self.api_keys:
            print("No Gemini API keys configured for embeddings.")
            return []
            
        for attempt in range(len(self.api_keys)):
            try:
                client = genai.Client(api_key=self.api_keys[self.current_key_idx])
                result = client.models.embed_content(
                    model=self.model_name,
                    contents=text,
                    config=types.EmbedContentConfig(
                        output_dimensionality=768
                    )
                )
                return result.embeddings[0].values
            except Exception as e:
                err_str = str(e).lower()
                if "429" in err_str or "quota" in err_str or "credits" in err_str or "400" in err_str:
                    print(f"Embedding failed due to limits/auth on key index {self.current_key_idx}. Rotating key...")
                    self.current_key_idx = (self.current_key_idx + 1) % len(self.api_keys)
                else:
                    print(f"Error generating embedding: {e}")
                    return []
                    
        print("All configured Gemini API keys failed for embeddings.")
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
                VALUES (%s, %s, NOW())
            """, (message_id, embedding))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error storing embedding: {e}")

    def semantic_search(self, query: str, limit: int = 5, exclude_session_id: str = None) -> List[Dict[str, Any]]:
        query_embedding = self.generate_embedding(query)
        if not query_embedding:
            return []
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if exclude_session_id:
                cursor.execute("""
                    SELECT m.id, m.role, m.content, m.created_at, 
                           (me.embedding <=> %s::vector) as distance
                    FROM message_embeddings me
                    JOIN messages m ON me.message_id = m.id
                    WHERE m.session_id IS DISTINCT FROM %s
                    ORDER BY distance ASC
                    LIMIT %s
                """, (query_embedding, exclude_session_id, limit))
            else:
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
