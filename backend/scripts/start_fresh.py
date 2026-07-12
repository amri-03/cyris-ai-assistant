import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app.db import get_db_connection

def wipe_database():
    print("WARNING: You are about to permanently wipe the database.")
    confirmation = input("Type 'YES' to confirm: ")
    
    if confirmation != "YES":
        print("Aborted.")
        return
        
    print("Wiping database tables...")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Truncate tables and reset identity columns
        cursor.execute("TRUNCATE TABLE message_embeddings CASCADE")
        cursor.execute("TRUNCATE TABLE messages RESTART IDENTITY CASCADE")
        cursor.execute("TRUNCATE TABLE sessions CASCADE")
        cursor.execute("TRUNCATE TABLE user_continuity CASCADE")
        cursor.execute("TRUNCATE TABLE behavioral_signals RESTART IDENTITY CASCADE")
        cursor.execute("TRUNCATE TABLE tasks RESTART IDENTITY CASCADE")
        cursor.execute("TRUNCATE TABLE goals RESTART IDENTITY CASCADE")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("PostgreSQL tables successfully truncated.")
    except Exception as e:
        print(f"Failed to wipe PostgreSQL tables: {e}")
        
    print("Deleting legacy SQLite database and JSON backups...")
    
    data_dir = Path(__file__).resolve().parent.parent / "data"
    files_to_delete = [
        "cyris.db",
        "database_backup.json",
        "conversation_memory.json",
        "runtime_history.json",
        "user_continuity.json"
    ]
    
    for filename in files_to_delete:
        file_path = data_dir / filename
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"Deleted {filename}")
            except Exception as e:
                print(f"Failed to delete {filename}: {e}")
                
    print("\nWipe complete! The slate is clean.")
    print("Restart your backend server to reinitialize the tables.")

if __name__ == "__main__":
    # If run in non-interactive mode (e.g. by an agent), we can pass --force
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        def input(prompt): return "YES"
    wipe_database()
