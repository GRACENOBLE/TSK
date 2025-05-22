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

def add_task (task: Task)-> Task:
    """
    Adds a new task to the database.
    The task object's ID will be updated with the generated database ID.
    """
    
    conn = _get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO tasks (description, created_at, due_date, completed) VALUES (?, ?, ?, ?)",
            (task.description, task.created_at, task.due_date, int(task.completed))
        )
        task.id = cursor.lastrowid 
        conn.commit()
        return task
    except sqlite3.Error as e:
        print(f"Error adding task: {e}")
        conn.rollback() 
        raise
    finally:
        conn.close()
        
def get_all_tasks(completed: Optional[bool] = None) -> List[Task]:
    """
    Retrieves all tasks from the database.
    Optionally filters by completion status.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    tasks = []
    try:
        query = "SELECT id, description, created_at, due_date, completed FROM tasks"
        params = []
        if completed is not None:
            query += " WHERE completed = ?"
            params.append(int(completed))

        query += " ORDER BY created_at DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        for row in rows:
            tasks.append(Task.from_db_row(row))
    except sqlite3.Error as e:
        print(f"Error retrieving tasks: {e}")
        raise
    finally:
        conn.close()
    return tasks

def get_task_by_id(task_id: int) -> Optional[Task]:
    """
    Retrieves a single task by its ID.
    Returns None if the task is not found.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    task = None
    try:
        cursor.execute(
            "SELECT id, description, created_at, due_date, completed FROM tasks WHERE id = ?",
            (task_id,)
        )
        row = cursor.fetchone()
        if row:
            task = Task.from_db_row(row)
    except sqlite3.Error as e:
        print(f"Error retrieving task by ID: {e}")
        raise
    finally:
        conn.close()
    return task

def update_task_completion(task_id: int, completed: bool) -> bool:
    """
    Updates the completion status of a task by its ID.
    Returns True if the task was updated, False otherwise (e.g., task not found).
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (int(completed), task_id)
        )
        conn.commit()
        return cursor.rowcount > 0 
    except sqlite3.Error as e:
        print(f"Error updating task completion: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
        
def delete_task(task_id: int) -> bool:
    """
    Deletes a task from the database by its ID.
    Returns True if the task was deleted, False otherwise (e.g., task not found).
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        conn.commit()
        return cursor.rowcount > 0 # Returns number of rows affected
    except sqlite3.Error as e:
        print(f"Error deleting task: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()