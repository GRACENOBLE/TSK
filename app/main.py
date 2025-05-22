from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.box import MINIMAL

from app.database import add_task, get_all_tasks, get_task_by_id, init_db, update_task_completion
from app.models import Task
from app.utils import parse_due_date

app = typer.Typer(help="A simple CLI task tracker.")
console = Console()

@app.callback()
def main_callback():
    """
    This callback is executed before any command.
    It ensures the database schema is initialized.
    """
    console.print("[dim]Initializing database...[/dim]", style="dim")
    init_db()
    console.print("[dim]Database initialized![/dim]", style="dim") 

@app.command()
def hello(name: str = "World"):
    """
    A simple command to say hello (for testing setup).
    """
    console.print(f"Hello, [bold green]{name}[/bold green]! Your To-Do app is ready.")

@app.command()
def add(
    description: str = typer.Argument(..., help="Description of the task."),
    due: Optional[str] = typer.Option(
        None, "--due", "-d",
        help="Optional due date (e.g., '2025-12-31', 'tomorrow', 'next week')."
    ),
):
    """
    Adds a new task to your to-do list.
    """
    parsed_due_date = parse_due_date(due) if due else None

    if due and parsed_due_date is None:
        console.print(f"[bold red]Error:[/bold red] Could not parse due date: '{due}'. Please use a valid format.")
        raise typer.Exit(code=1)

    new_task = Task(description=description, due_date=parsed_due_date)
    try:
        add_task(new_task)
        console.print(f"[green]Added task:[/green] [bold]{new_task.description}[/bold] (ID: {new_task.id})")
        if new_task.due_date:
            console.print(f"  [dim]Due:[/dim] {new_task.due_date}")
    except Exception as e:
        console.print(f"[bold red]Failed to add task:[/bold red] {e}")
        raise typer.Exit(code=1)
    
@app.command(name="list")
def list_tasks(
    all_tasks: bool = typer.Option(False, "--all", "-a", help="Show all tasks (including completed ones)."),
    pending_only: bool = typer.Option(False, "--pending", "-p", help="Show only pending tasks."),
    completed_only: bool = typer.Option(False, "--completed", "-c", help="Show only completed tasks."),
):
    """
    Lists tasks in your to-do list.
    By default, shows only pending tasks.
    """
    if sum([all_tasks, pending_only, completed_only]) > 1:
        console.print("[bold red]Error:[/bold red] Please choose only one of --all, --pending, or --completed.")
        raise typer.Exit(code=1)

    filter_status: Optional[bool] = None
    if pending_only:
        filter_status = False
    elif completed_only:
        filter_status = True
    elif not all_tasks:
        filter_status = False

    try:
        tasks = get_all_tasks(completed=filter_status)

        if not tasks:
            console.print("[yellow]No tasks found.[/yellow]")
            if filter_status is False:
                console.print("[dim]Try adding a task with 'todo add \"My new task\"' or listing all with 'todo list --all'.[/dim]")
            return

        table = Table(
            box=MINIMAL,
            show_header=True,
            header_style="bold magenta",
            title="[bold green]Your To-Do List[/bold green]"
        )
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Description", style="white")
        table.add_column("Created", style="dim")
        table.add_column("Due Date", style="yellow")
        table.add_column("Status", style="bold")

        for task in tasks:
            status = Text("✅ Completed", style="green") if task.completed else Text("⏳ Pending", style="orange1")
            description_style = "strike dim" if task.completed else "white" # Strikethrough completed tasks

            table.add_row(
                str(task.id),
                Text(task.description, style=description_style),
                task.created_at[:10], # Show only date part
                task.due_date if task.due_date else "[dim]-[/dim]",
                status
            )
        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Failed to list tasks:[/bold red] {e}")
        raise typer.Exit(code=1)
    
@app.command()
def complete(
    task_id: int = typer.Argument(..., help="The ID of the task to mark as complete."),
):
    """
    Marks a task as complete.
    """
    try:
        task = get_task_by_id(task_id)
        if not task:
            console.print(f"[bold red]Error:[/bold red] Task with ID [cyan]{task_id}[/cyan] not found.")
            raise typer.Exit(code=1)

        if task.completed:
            console.print(f"[yellow]Task [cyan]{task_id}[/cyan] '[bold]{task.description}[/bold]' is already completed.[/yellow]")
            return

        updated = update_task_completion(task_id, True)
        if updated:
            console.print(f"[green]Marked task [cyan]{task_id}[/cyan] '[bold]{task.description}[/bold]' as complete. ✅[/green]")
        else:
            console.print(f"[bold red]Error:[/bold red] Could not mark task [cyan]{task_id}[/cyan] as complete.")
            raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"[bold red]Failed to complete task:[/bold red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
    
