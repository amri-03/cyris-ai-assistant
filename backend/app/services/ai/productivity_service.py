from typing import List, Dict, Any
from app.db import get_db_connection

class ProductivityService:
    def create_goal(self, title: str, description: str = "") -> int:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO goals (title, description, created_at, updated_at)
            VALUES (%s, %s, datetime('now'), datetime('now'))
            RETURNING id
        """, (title, description))
        goal_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return goal_id

    def update_goal_progress(self, goal_id: int, progress: int, status: str = 'active'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE goals 
            SET progress = %s, status = %s, updated_at = datetime('now')
            WHERE id = %s
        """, (progress, status, goal_id))
        conn.commit()
        cursor.close()
        conn.close()

    def add_task_to_goal(self, goal_id: int, description: str) -> int:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (goal_id, description, created_at, updated_at)
            VALUES (%s, %s, datetime('now'), datetime('now'))
            RETURNING id
        """, (goal_id, description))
        task_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return task_id

    def complete_task(self, task_id: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks
            SET is_completed = TRUE, updated_at = datetime('now')
            WHERE id = %s
        """, (task_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def get_active_goals_with_tasks(self) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, description, status, progress, created_at
            FROM goals
            WHERE status = 'active'
        """)
        goals = []
        for g_row in cursor.fetchall():
            goal = {
                "id": g_row['id'],
                "title": g_row['title'],
                "description": g_row['description'],
                "status": g_row['status'],
                "progress": g_row['progress'],
                "tasks": []
            }
            cursor.execute("""
                SELECT id, description, is_completed
                FROM tasks
                WHERE goal_id = %s
            """, (goal["id"],))
            for t_row in cursor.fetchall():
                goal["tasks"].append({
                    "id": t_row['id'],
                    "description": t_row['description'],
                    "is_completed": t_row['is_completed']
                })
            goals.append(goal)
            
        cursor.close()
        conn.close()
        return goals
