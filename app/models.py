import datetime
from typing import Optional

class Task:
    def __init__(
        self,
        description: str,
        due_date: Optional[str] = None,
        completed: bool = False,
        id: Optional[int] = None,
        created_at: Optional[str] = None
    ):
        self.id = id
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.created_at = created_at

    def __repr__(self):
            """String representation for debugging."""
            status = "✅" if self.completed else "⏳"
            due = f" (Due: {self.due_date})" if self.due_date else ""
            return f"{status} Task {self.id}: {self.description}{due}"
            
    def to_dict(self):
        """Converts Task object to a dictionary (useful for debugging or future extensions)."""
        return {
            "id": self.id,
            "description": self.description,
            "created_at": self.created_at,
            "due_date": self.due_date,
            "completed": self.completed
        }
        
    @classmethod
    def from_db_row(cls, row: dict):
        """Creates a Task object from a database row (assuming row_factory is set to sqlite3.Row)."""
        return cls(
            id=row['id'],
            description=row['description'],
            created_at=row['created_at'],
            due_date=row['due_date'],
            completed=bool(row['completed']) # SQLite stores booleans as 0 or 1
        )