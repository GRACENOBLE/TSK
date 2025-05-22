import typer
from rich.console import Console
# from rich.table import Table # Will be used later for list command

from app.database import init_db # Import the init_db function
# from todo_app.models import Task # Will be used later
# from todo_app.utils import parse_due_date, get_today_str # Will be used later

app = typer.Typer(help="A simple CLI task tracker.")
console = Console()

@app.callback()
def main_callback():
    """
    This callback is executed before any command.
    It ensures the database schema is initialized.
    """
    console.print("[dim]Initializing database...[/dim]", style="dim") # Optional: provide user feedback
    init_db()
    console.print("[dim]Database initialized![/dim]", style="dim") # Optional: provide user feedback

# --- Example Command (to demonstrate initialization) ---
@app.command()
def hello(name: str = "World"):
    """
    A simple command to say hello (for testing setup).
    """
    console.print(f"Hello, [bold green]{name}[/bold green]! Your To-Do app is ready.")

# --- Future Commands (add, list, complete, delete, etc.) will go here ---
# @app.command()
# def add(...):
#     # ...

# @app.command()
# def list(...):
#     # ...

if __name__ == "__main__":
    app()