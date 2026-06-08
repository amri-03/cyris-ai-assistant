import json
import os
import sqlite3
from datetime import datetime
from app.db import get_db_connection
from app.memory.continuity_extractor import ContinuityExtractor

class MemoryReconciler:

    def __init__(self):
        self.rule_extractor = ContinuityExtractor()

    def rebuild_memory_from_history(self, ai_provider_manager):
        try:
            print("Starting memory reconciliation...")
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Fetch all messages
            cursor.execute(
                "SELECT role, content, created_at FROM messages ORDER BY id ASC"
            )
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                print("No history found in database. Skipping reconciliation.")
                return {"status": "skipped", "reason": "No messages in history"}

            # Filter messages to keep only relevant context (Token Efficiency)
            relevant_messages = []
            
            for i in range(len(rows)):
                row = rows[i]
                role = row["role"]
                content = row["content"]
                created_at = row["created_at"]
                
                # If it's a user message, check if it contains continuity topics
                if role == "user":
                    if self.rule_extractor.extract_continuity(content):
                        # Add user message
                        relevant_messages.append(f"[{created_at}] User: {content}")
                        # Add subsequent assistant reply if available
                        if i + 1 < len(rows) and rows[i+1]["role"] == "assistant":
                            next_row = rows[i+1]
                            relevant_messages.append(f"[{next_row['created_at']}] Assistant: {next_row['content']}")
            
            if not relevant_messages:
                print("No relevant continuity topics found in history. Skipping reconciliation.")
                return {"status": "skipped", "reason": "No matching continuity topics"}
                
            history_str = "\n".join(relevant_messages)
            
            # Build prompt
            prompt = f"""
            You are performing a full memory reconciliation and cleanup for a user.
            Below is the filtered chronological history of the user's conversations over the past few weeks, with timestamps:
            
            {history_str}
            
            Your task is to analyze this entire history and extract ALL meaningful long-term continuity information.
            
            Normalize similar concepts into stable identities.
            
            Valid continuity types:
            - goal
            - focus_area
            - struggle
            - interest
            - project
            - academic_context
            - career_direction
            - user_preference
            
            Ensure that:
            1. Academic timeline details (institutions, dates, transfers, gaps) should be merged into a single detailed 'academic_status' item that preserves chronological progression.
            2. Career directions should be captured in 'career_direction' items.
            3. Active projects should be captured with their relevant tech stack and details.
            4. Focus areas should be captured cleanly without duplication.
            
            Return ONLY valid JSON in the format:
            {{
                "continuity_items": [
                    {{
                        "identity": "...",
                        "type": "...",
                        "content": "...",
                        "importance": "low | medium | high"
                    }}
                ]
            }}
            """
            
            # Generate response from LLM (using the active provider manager)
            # Reconcile memory is run in a background thread or manually, using the active client
            print("Sending reconciliation request to LLM...")
            # We use add_to_history=False so the reconciliation query does not clutter the chat history
            raw_resp = ai_provider_manager.ai_client.generate_response(prompt, add_to_history=False)
            normalized = ai_provider_manager.normalizer.normalize_response(raw_resp)
            if normalized.get("status") != "success":
                raise Exception(normalized.get("error", "Failed to generate response from AI client"))
            response_text = normalized["response"]
            
            # Robust JSON extraction
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}")
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx + 1]
            else:
                json_str = response_text
                
            cleaned = json_str.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)
            
            items_to_save = parsed.get("continuity_items", [])
            if not items_to_save:
                print("No continuity items extracted during reconciliation.")
                return {"status": "success", "items_extracted": 0}
                
            timestamp_str = datetime.now().isoformat()
            
            # Save to SQLite
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Retire all existing active items
            cursor.execute("UPDATE user_continuity SET retired = 1, last_updated = ? WHERE retired = 0", (timestamp_str,))
            
            # Save newly extracted items
            for item in items_to_save:
                identity = item.get("identity")
                if not identity:
                    continue
                    
                # Calculate priority
                priority_map = {
                    "career_direction": 5,
                    "goal": 4,
                    "focus_area": 4,
                    "project": 4,
                    "academic_context": 3,
                    "struggle": 5,
                    "interest": 2
                }
                priority = priority_map.get(item["type"], 3)
                if item.get("importance") == "high":
                    priority = min(5, priority + 1)
                elif item.get("importance") == "low":
                    priority = max(1, priority - 1)
                    
                cursor.execute("""
                    INSERT INTO user_continuity (identity, type, content, importance, priority, retired, created_at, last_updated)
                    VALUES (?, ?, ?, ?, ?, 0, ?, ?)
                    ON CONFLICT(identity) DO UPDATE SET 
                        type=excluded.type, content=excluded.content, importance=excluded.importance, 
                        priority=excluded.priority, retired=0, last_updated=excluded.last_updated
                """, (identity, item["type"], item["content"], item.get("importance", "medium"), priority, timestamp_str, timestamp_str))
                
            conn.commit()
            conn.close()
            print(f"Memory reconciliation completed. Re-extracted {len(items_to_save)} active items.")
            return {"status": "success", "items_extracted": len(items_to_save)}
            
        except Exception as e:
            print(f"Error during memory reconciliation: {e}")
            return {"status": "error", "error": str(e)}
