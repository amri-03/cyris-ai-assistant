import sqlite3
import threading
from datetime import datetime

from app.db import get_db_connection
from app.services.ai.continuity_ai_extractor import ContinuityAIExtractor
from app.memory.continuity_extractor import ContinuityExtractor


class ContinuityMemoryService:
    _db_lock = threading.Lock()

    def __init__(self):
        self.extractor = ContinuityAIExtractor()
        self.rule_extractor = ContinuityExtractor()

    def load_memory(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT identity, type, content, importance, priority, created_at, last_updated FROM user_continuity WHERE retired = 0"
            )
            rows = cursor.fetchall()
            conn.close()
            
            items = []
            for row in rows:
                items.append({
                    "identity": row["identity"],
                    "type": row["type"],
                    "content": row["content"],
                    "importance": row["importance"],
                    "priority": row["priority"],
                    "created_at": row["created_at"],
                    "last_updated": row["last_updated"]
                })
            
            return {"continuity_items": items}
            
        except Exception:
            return {"continuity_items": []}

    def delete_continuity_item(self, identity: str):
        try:
            with self._db_lock:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                timestamp_str = datetime.now().isoformat()
                cursor.execute(
                    "UPDATE user_continuity SET retired = 1, last_updated = ? WHERE identity = ?",
                    (timestamp_str, identity)
                )
                
                conn.commit()
                conn.close()
            return True
        except Exception:
            return False

    def save_continuity(self, ai_client, message: str):
        try:
            # Construct conversation history context for the extractor
            from app.memory.conversation_history_service import ConversationHistoryService
            history_service = ConversationHistoryService()
            history_messages = history_service.get_messages()

            # Format the last 5 messages for context
            context_lines = []
            for msg in history_messages[-5:]:
                role = "User" if msg["role"] == "user" else "Assistant"
                context_lines.append(f"{role}: {msg['content']}")
            
            if context_lines:
                history_context = "\n".join(context_lines)
            else:
                history_context = f"User: {message}"

            # Token Efficiency: pre-filter message using rule-based keyword check
            if not self.rule_extractor.extract_continuity(history_context):
                return

            memory = self.load_memory()
            existing_items = memory.get("continuity_items", [])

            extracted = self.extractor.extract_structured_continuity(
                ai_client,
                history_context,
                existing_items
            )

            items_to_save = extracted.get("continuity_items", [])
            if not items_to_save:
                return

            timestamp_str = datetime.now().isoformat()
            
            with self._db_lock:
                conn = get_db_connection()
                cursor = conn.cursor()

                for item_data in items_to_save:
                    identity = item_data.get("identity")
                    if not identity:
                        continue

                    # Process supersedes: check and archive
                    if item_data.get("supersedes"):
                        for superseded_id in item_data["supersedes"]:
                            # Fetch superseded item
                            cursor.execute(
                                "SELECT type, content FROM user_continuity WHERE identity = ? AND retired = 0",
                                (superseded_id,)
                            )
                            sup_row = cursor.fetchone()
                            
                            if sup_row:
                                # Type Guard: Only allow superseding if type or identity matches
                                if sup_row["type"] == item_data["type"] or superseded_id == identity:
                                    old_content = sup_row["content"]
                                    new_content = item_data["content"]
                                    
                                    timeline_keywords = ["mit", "transfer", "gap", "12th", "2023", "2024", "2025", "getting in", "getting good", "getting dangerous", "getting free"]
                                    has_old_timeline = any(kw in old_content.lower() for kw in timeline_keywords)
                                    has_new_timeline = any(kw in new_content.lower() for kw in timeline_keywords)
                                    
                                    if has_old_timeline and not has_new_timeline:
                                        item_data["content"] = old_content
                                    elif has_old_timeline and has_new_timeline:
                                        # Protect specific details (gap year, college transfer) from being lost
                                        important_timeline_kws = ["mit", "parul", "gap", "transfer", "2023", "2024", "2025"]
                                        old_kws = [kw for kw in important_timeline_kws if kw in old_content.lower()]
                                        new_kws = [kw for kw in important_timeline_kws if kw in new_content.lower()]
                                        missing_kws = [kw for kw in old_kws if kw not in new_kws]
                                        if missing_kws:
                                            if "icse" in new_content.lower() or "isc" in new_content.lower():
                                                item_data["content"] = f"{new_content}. College/gap details: {old_content}"
                                            else:
                                                item_data["content"] = old_content
                                    
                                    # Retire the superseded item
                                    cursor.execute(
                                        "UPDATE user_continuity SET retired = 1, last_updated = ? WHERE identity = ?",
                                        (timestamp_str, superseded_id)
                                    )

                    # Check if the target item already exists
                    cursor.execute(
                        "SELECT priority, content FROM user_continuity WHERE identity = ?",
                        (identity,)
                    )
                    existing_row = cursor.fetchone()

                    if existing_row:
                        old_content = existing_row["content"]
                        new_content = item_data["content"]
                        
                        timeline_keywords = ["mit", "transfer", "gap", "12th", "2023", "2024", "2025", "getting in", "getting good", "getting dangerous", "getting free"]
                        has_old_timeline = any(kw in old_content.lower() for kw in timeline_keywords)
                        has_new_timeline = any(kw in new_content.lower() for kw in timeline_keywords)
                        
                        if has_old_timeline and not has_new_timeline:
                            item_data["content"] = old_content
                        elif has_old_timeline and has_new_timeline:
                            important_timeline_kws = ["mit", "parul", "gap", "transfer", "2023", "2024", "2025"]
                            old_kws = [kw for kw in important_timeline_kws if kw in old_content.lower()]
                            new_kws = [kw for kw in important_timeline_kws if kw in new_content.lower()]
                            missing_kws = [kw for kw in old_kws if kw not in new_kws]
                            if missing_kws:
                                if "icse" in new_content.lower() or "isc" in new_content.lower():
                                    item_data["content"] = f"{new_content}. College/gap details: {old_content}"
                                else:
                                    item_data["content"] = old_content

                        # Calculate new priority
                        new_priority = min(5, (existing_row["priority"] or 3) + 1)
                        
                        cursor.execute("""
                            UPDATE user_continuity 
                            SET type = ?, content = ?, importance = ?, priority = ?, retired = 0, last_updated = ?
                            WHERE identity = ?
                        """, (item_data["type"], item_data["content"], item_data["importance"], new_priority, timestamp_str, identity))
                    else:
                        priority = self.calculate_priority(item_data["type"], item_data["importance"])
                        cursor.execute("""
                            INSERT INTO user_continuity (identity, type, content, importance, priority, retired, created_at, last_updated)
                            VALUES (?, ?, ?, ?, ?, 0, ?, ?)
                        """, (identity, item_data["type"], item_data["content"], item_data["importance"], priority, timestamp_str, timestamp_str))

                conn.commit()
                conn.close()

        except Exception as e:
            print(f"Error saving continuity in SQLite: {e}")

    def build_continuity_context(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT content, importance FROM user_continuity WHERE retired = 0 ORDER BY priority DESC LIMIT 10"
            )
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                return ""
                
            formatted_items = []
            for row in rows:
                formatted_items.append(f'- {row["content"]} (importance: {row["importance"]})')
            
            return "Known user continuity:\n" + "\n".join(formatted_items)
            
        except Exception:
            return ""

    def build_priority_briefing(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT identity, content FROM user_continuity WHERE retired = 0 ORDER BY priority DESC LIMIT 20"
            )
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                return ""
                
            briefing = []
            for row in rows:
                briefing.append(f'- {row["identity"]}: {row["content"]}')
                
            return "Current important continuity areas:\n" + "\n".join(briefing)
            
        except Exception:
            return ""

    def calculate_priority(self, continuity_type, importance):
        priority_map = {
            "career_direction": 5,
            "goal": 4,
            "focus_area": 4,
            "project": 4,
            "academic_context": 3,
            "struggle": 5,
            "interest": 2
        }
        importance_bonus = {
            "high": 1,
            "medium": 0,
            "low": -1
        }
        base_priority = priority_map.get(continuity_type, 1)
        adjustment = importance_bonus.get(importance, 0)
        return max(1, min(base_priority + adjustment, 5))