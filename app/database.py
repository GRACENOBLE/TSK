import sqlite3
from typing import List, Optional
from app.models import Task

DB_FILE = 'tasks.db'

def _get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.
    If DB_FILE does not exist, it will be created.
    Uses row_factory to allow column access by name.
    """
    
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
    
def init_db():
    """
    Initializes the database schema by creating the 'tasks' table if it doesn't exist.
    This function should be called once at the start of the application.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            created_at TEXT NOT NULL,
            due_date TEXT, -- Stored as 'YYYY-MM-DD' string
            completed INTEGER NOT NULL DEFAULT 0 -- SQLite stores booleans as 0 (False) or 1 (True)
        )
    """)
    conn.commit()
    conn.close()
# end def