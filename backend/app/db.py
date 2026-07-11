import os
import psycopg2
from psycopg2.extras import DictCursor
from pgvector.psycopg2 import register_vector
from dotenv import load_dotenv

load_dotenv()

# We expect POSTGRES_URL in environment variables, or fallback to the local docker instance we setup
DB_URL = os.getenv("POSTGRES_URL", "postgresql://cyris:cyris_password@localhost:5433/cyris")

def get_db_connection():
    conn = psycopg2.connect(DB_URL, cursor_factory=DictCursor)
    # Register pgvector type on connection
    try:
        register_vector(conn)
    except psycopg2.ProgrammingError:
        pass # vector extension might not be created yet during init
    return conn

def init_db():
    conn = get_db_connection()
    conn.commit()
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Check if messages table exists
    cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'messages');")
    db_new = not cursor.fetchone()[0]

    # Create vector extension for semantic search
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    # Re-register vector since it might be just created
    register_vector(conn)
    
    # Create messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            session_active INTEGER DEFAULT 1,
            feedback TEXT
        )
    """)
    
    # Create user_continuity table
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
    
    # Create behavioral_signals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS behavioral_signals (
            id SERIAL PRIMARY KEY,
            signal_type TEXT NOT NULL,
            signal_value TEXT NOT NULL,
            context TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # Create goals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'active',
            progress INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            goal_id INTEGER REFERENCES goals(id) ON DELETE CASCADE,
            description TEXT NOT NULL,
            is_completed BOOLEAN DEFAULT FALSE,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Create message_embeddings table (Semantic Memory)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS message_embeddings (
            id SERIAL PRIMARY KEY,
            message_id INTEGER REFERENCES messages(id) ON DELETE CASCADE,
            embedding vector(3072) NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    # Note: HNSW index omitted because 3072 dimensions exceeds pgvector HNSW default limit of 2000

    cursor.close()
    conn.close()
    
    # Note: Auto-migration of old sqlite data is handled manually via the migrate script to prevent accidental destructive actions
    if db_new:
        print("Database initialized successfully.")
