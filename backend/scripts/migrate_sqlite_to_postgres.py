import os
import sqlite3
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SQLITE_DB_FILE = Path(__file__).resolve().parent / "backend" / "data" / "cyris.db"
POSTGRES_DB_URL = os.getenv("POSTGRES_URL", "postgresql://cyris:cyris_password@localhost:5433/cyris")

def migrate_data():
    if not SQLITE_DB_FILE.exists():
        print(f"SQLite DB not found at {SQLITE_DB_FILE}. Nothing to migrate.")
        return

    print("Connecting to SQLite database...")
    sqlite_conn = sqlite3.connect(SQLITE_DB_FILE)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()

    print("Connecting to PostgreSQL database...")
    try:
        pg_conn = psycopg2.connect(POSTGRES_DB_URL)
        pg_cursor = pg_conn.cursor()
    except Exception as e:
        print(f"Failed to connect to PostgreSQL: {e}")
        return

    # Check if messages table exists in PG
    try:
        pg_cursor.execute("SELECT COUNT(*) FROM messages")
        msg_count = pg_cursor.fetchone()[0]
        if msg_count > 0:
            print("PostgreSQL database is already populated. Migration aborted to prevent duplication.")
            return
    except psycopg2.errors.UndefinedTable:
        # Table doesn't exist, we need to initialize the db first
        pg_conn.rollback()
        import sys
        sys.path.append(str(Path(__file__).resolve().parent / "backend"))
        from app.db import init_db
        print("Initializing PostgreSQL database schemas...")
        init_db()
        pg_cursor.execute("SELECT COUNT(*) FROM messages")

    print("Migrating 'messages' table...")
    sqlite_cursor.execute("SELECT id, role, content, created_at, session_active, feedback FROM messages")
    messages = sqlite_cursor.fetchall()
    
    # We use batch inserts for efficiency
    if messages:
        # Since we use SERIAL for id in pg, and we want to preserve old IDs, we should insert them manually
        # and then reset the sequence
        for msg in messages:
            pg_cursor.execute("""
                INSERT INTO messages (id, role, content, created_at, session_active, feedback)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (msg['id'], msg['role'], msg['content'], msg['created_at'], msg['session_active'], msg['feedback']))
        
        # Reset the primary key sequence for messages
        pg_cursor.execute("SELECT setval(pg_get_serial_sequence('messages', 'id'), COALESCE(MAX(id), 1)) FROM messages")
        print(f"Migrated {len(messages)} messages.")

    print("Migrating 'user_continuity' table...")
    sqlite_cursor.execute("SELECT identity, type, content, importance, priority, retired, created_at, last_updated FROM user_continuity")
    continuity_records = sqlite_cursor.fetchall()
    
    if continuity_records:
        for record in continuity_records:
            pg_cursor.execute("""
                INSERT INTO user_continuity (identity, type, content, importance, priority, retired, created_at, last_updated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (identity) DO NOTHING
            """, (record['identity'], record['type'], record['content'], record['importance'], record['priority'], record['retired'], record['created_at'], record['last_updated']))
        print(f"Migrated {len(continuity_records)} user_continuity records.")

    print("Migrating 'behavioral_signals' table...")
    try:
        sqlite_cursor.execute("SELECT id, signal_type, signal_value, context, created_at FROM behavioral_signals")
        signals = sqlite_cursor.fetchall()
        if signals:
            for sig in signals:
                pg_cursor.execute("""
                    INSERT INTO behavioral_signals (id, signal_type, signal_value, context, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (sig['id'], sig['signal_type'], sig['signal_value'], sig['context'], sig['created_at']))
            pg_cursor.execute("SELECT setval(pg_get_serial_sequence('behavioral_signals', 'id'), COALESCE(MAX(id), 1)) FROM behavioral_signals")
            print(f"Migrated {len(signals)} behavioral_signals.")
    except sqlite3.OperationalError:
        print("Table 'behavioral_signals' does not exist in SQLite DB. Skipping.")

    pg_conn.commit()
    print("Migration completed successfully!")

    sqlite_cursor.close()
    sqlite_conn.close()
    pg_cursor.close()
    pg_conn.close()

if __name__ == "__main__":
    migrate_data()
