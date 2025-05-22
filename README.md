# [TSK](https://github.com/GRACENOBLE/TSK.git)
![tasks](/public/images/tasks.png)
A simple yet powerful CLI application for managing your daily tasks. Built with Python and SQLite, it allows you to add, list, mark tasks as complete, and delete tasks directly from your terminal.

## Table of Contents

- [Features](#1-features)
- [Technologies Used](#2-technologies-used)
- [Project Structure](#3-project-structure)
- [Getting Started](#4-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Initialization](#database-initialization)
- [Usage](#5-usage)
  - [tsk Command Overview](#tsk-command-overview)
  - [add command](#add-command)
  - [list command](#list-command)
  - [complete command](#complete-command)
  - [delete command](#delete-command)
- [Getting Help](#getting-help)
- [Future Enhancements](#6-future-enhancements)
- [License](#7-license)
- [Additional considerations](#8-additional-considerations)
- [contribution](#8-contribution)

## 1. Features

- **Add Tasks**: Quickly add new tasks with optional due dates.
- **List Tasks**: View your tasks, filtered by pending, completed, or all.
- **Mark Complete**: Easily mark tasks as done.
- **Delete Tasks**: Remove tasks from your list.
- **Persistent Storage**: Tasks are saved locally using SQLite, so they persist across sessions.
- **User-Friendly Interface**: Clear, colorful output powered by Rich.

## 2. Technologies Used

- **Python 3.8+**: The core programming language.
- **Typer**: A modern, type-hint-driven library for building robust and user-friendly command-line interfaces.
- **Rich**: A fantastic library for beautiful terminal rendering, providing colors, tables, and rich text.
- **SQLite3**: Python's built-in module for interacting with SQLite, a lightweight, file-based relational database, used for persistent task storage.
- **python-dateutil**: A powerful library for parsing human-readable date and time strings.

## 3. Project Structure

```
todo_cli/
├── .venv/                   # Python Virtual Environment (ignored by Git)
├── app/                     # Main application package
│   ├── __init__.py          # Makes 'app' a Python package
│   ├── main.py              # Main CLI entry point, defines commands
│   ├── database.py          # Handles all SQLite database interactions
│   ├── models.py            # Defines the 'Task' data structure
│   └── utils.py             # Helper functions (e.g., date parsing, validation)
├── tests/                   # Unit and integration tests
│   ├── __init__.py
│   ├── test_database.py     # Tests for database.py functions
│   └── test_main.py         # Tests for CLI commands
├── .gitignore               # Specifies files/directories to be ignored by Git
├── README.md                # This documentation file
├── requirements.txt         # Lists Python dependencies
└── pyproject.toml           # Defines project metadata and build configuration

```

## 4. Getting Started

Follow these steps to set up and run the To-Do CLI application on your local machine.

### Prerequisites

- **Python 3.8+**: Download from [python.org](https://www.python.org/)
- **Git**: Download from [git-scm.com](https://git-scm.com/)

### Installation

**Clone the Repository:**

```bash
git clone https://github.com/GRACENOBLE/todo_cli.git
```

![image](/public/images/cloning.png)

**Navigate to the Project Directory:**

```bash
cd todo_cli
```

![image](/public/images/cd.png)

**Create and Activate a Virtual Environment:**

```bash
# Create the virtual environment
python -m venv .venv
#or
python3 -m venv .venv

# Activate the virtual environment:
# On macOS / Linux:
source .venv/bin/activate

# On Windows (Command Prompt):
.venv\Scripts\activate.bat

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

```

You should see `(.venv)` or similar at the beginning of your terminal prompt, indicating the virtual environment is active.
![Activate the environment](/public/images/activate_environment.png)

**Install Project in Editable Mode:**

```bash
pip install -e .
```

![install in edit mode](/public/images/install_in_edit_mode.png)

### Database Initialization

This application uses a local SQLite database, stored in a single file named `tasks.db`. You will not find this file in the Git repository as it's generated locally for each user.

The first time you run any `tsk` command (e.g., `tsk add "My first task"`), the application will automatically:

- Create the `tasks.db` file in your project's root directory if it doesn't already exist.
- Set up the necessary `tasks` table structure inside that `tasks.db` file.

![database](/public/images/database.png)

This ensures a clean and automatic setup without any manual database configuration required from your end.

## 5. Usage

Once installed, you can start using the `tsk` command.

### tsk Command Overview

All interactions with the To-Do CLI app start with the `tsk` command, followed by a subcommand and its arguments/options.

### add command

Adds a new task to your to-do list.

```bash
tsk add "Your task description here" [--due <date>]
```

- `<description>`: (Required) The text of your task.
- `-due` or `d`: (Optional) Specify a due date.

**Accepted formats**: `YYYY-MM-DD` (e.g., `2025-12-31`), `today`, `tomorrow`, `next week`, `next month`, `next year`.

**Examples:**

```bash
# Add a simple task
tsk add "Finish project report"

# Add a task due on a specific date
tsk add "Schedule team meeting" --due 2025-06-01

# Add a task due tomorrow
tsk add "Call client about proposal" -d tomorrow

# Add a task due next week
tsk add "Plan weekend trip" -d "next week"
```

### list command

Lists tasks in your to-do list. By default, it shows only pending tasks.
![list yoour todos](/public/images/list.png)

```bash
tsk list [--all | --pending | --completed]
```

- `-all` or `a`: Show all tasks (including completed ones).
- `-pending` or `p`: Show only pending tasks (default behavior).
- `-completed` or `c`: Show only completed tasks.

Note: You can only use one of `--all`, `--pending`, or `--completed` at a time.

**Examples:**

```bash
# List all pending tasks (default)
tsk list

# List all tasks (pending and completed)
tsk list --all

# List only completed tasks
tsk list --completed
```

### complete command

Marks a task as complete.

```bash
tsk complete <task_id>
```

- `<task_id>`: (Required) The numerical ID of the task to mark as complete. You can find the task ID using the `list` command.

**Examples:**

```bash
# Mark task with ID 1 as complete
tsk complete 1

# If task 1 was already complete
tsk complete 1
# Output: Task 1 'Finish project report' is already completed.
```

![complete task](/public/images/complete.png)

### delete command

Deletes a task from the to-do list.

```bash
tsk delete <task_id> [--force]
```

- `<task_id>`: (Required) The numerical ID of the task to delete.
- `-force` or `f`: (Optional) Skip the confirmation prompt and delete immediately.

**Examples:**

```bash
# Delete task with ID 3 (will prompt for confirmation)
tsk delete 3

# Delete task with ID 2 without confirmation
tsk delete 2 --force
```

![delete task](/public/images/delete.png)

## Getting Help

You can always get help for the main application or specific commands using the `--help` flag:

```bash
# Get help for the main application
tsk --help

# Get help for the 'add' command
tsk add --help
```

![ask for help](/public/images/help.png)

## 6. Future Enhancements

Here are some ideas for extending this application:

- **Edit Task**: Implement a command to modify task descriptions or due dates.
- **Search/Filter**: More advanced filtering options (e.g., by keyword, by date range).
- **Priorities**: Add a priority level to tasks.
- **Categories/Tags**: Organize tasks into categories or with tags.
- **Export/Import**: Allow exporting tasks to CSV/JSON or importing from them.
- **Undo/Redo**: Implement an undo/redo functionality.

## 7. License

This project is open-source and available under the [MIT License](/LICENSE).

## 8. Additional considerations

Should you want to interact with your database of tasks, consider installing the db browser for sqlite
![sqlite db browser](/public/images/sqlite_db_browser.png)
## 9. Contribution
Just make a pr dude 😎

## 10. Roadmap.sh
This challenge was originally atarted by [Roadmap.sh](https://roadmap.sh/projects/task-tracker)