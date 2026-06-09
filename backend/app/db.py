import sqlite3
from pathlib import Path

DB_FILE = Path("data/cyris.db")

def get_db_connection():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if messages table exists to detect newly initialized DB
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
    db_new = cursor.fetchone() is None
    
    # Create messages table (stores the complete history)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            session_active INTEGER DEFAULT 1,
            feedback TEXT
        )
    """)
    
    # Ensure feedback column exists
    try:
        cursor.execute("ALTER TABLE messages ADD COLUMN feedback TEXT")
    except Exception:
        pass
    
    # Create user_continuity table (stores long-term memories)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_continuity (
            identity TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            content TEXT NOT NULL,
            importance TEXT NOT NULL,
            priority INTEGER NOT NULL,
            retired INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            last_updated TEXT NOT NULL
        )
    """)
    
    # Create behavioral_signals table (stores timestamped mood/energy observations)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS behavioral_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signal_type TEXT NOT NULL,
            signal_value TEXT NOT NULL,
            context TEXT,
            created_at TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    
    # Auto-migrate existing JSON data if the DB was just initialized
    if db_new:
        try:
            import sys
            # Add backend root directory to path if needed
            sys.path.append(str(Path(__file__).parent.parent))
            from migrate_json_to_sqlite import run_migration
            run_migration()
        except Exception as e:
            print(f"Auto-migration failed: {e}")
