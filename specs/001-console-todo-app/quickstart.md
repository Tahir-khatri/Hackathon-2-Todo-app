# Quickstart: In-Memory Python Console Todo App (Phase I)

**Date**: 2026-01-14
**Feature**: 001-console-todo-app

## Prerequisites

- Python 3.13 or higher
- UV package manager (optional, for dependency management)
- Terminal/Command Prompt access

### Verify Python Installation

```bash
python --version
# Expected: Python 3.13.x or higher
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hackathon-2-evolution-of-todo
```

### 2. Checkout the Feature Branch

```bash
git checkout 001-console-todo-app
```

### 3. Setup with UV (Recommended)

```bash
# Install UV if not already installed
pip install uv

# Create virtual environment and install dependencies
uv venv
uv pip install -e .
```

### 4. Alternative: Setup with pip

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install in development mode
pip install -e .
```

---

## Running the Application

### Option 1: As a Module

```bash
python -m src.main
```

### Option 2: Direct Script

```bash
python src/main.py
```

---

## Usage Guide

### Main Menu

When you start the application, you'll see:

```
========== Todo App ==========
1. Add Task
2. View All Tasks
3. Mark Task Complete
4. Update Task
5. Delete Task
6. Exit
==============================
Enter your choice:
```

### Adding a Task

1. Select option `1`
2. Enter a task description (1-500 characters)
3. See confirmation with assigned task ID

```
Enter your choice: 1
Enter task description: Buy groceries
✓ Task added successfully! (ID: 1)
```

### Viewing All Tasks

1. Select option `2`
2. See all tasks with their ID, status, and description

```
Enter your choice: 2

========== Your Tasks ==========
[ ] 1. Buy groceries
[x] 2. Call mom
================================
Total: 2 tasks (1 pending, 1 completed)
```

### Marking a Task Complete

1. Select option `3`
2. Enter the task ID
3. See confirmation

```
Enter your choice: 3
Enter task ID: 1
✓ Task marked as complete!
```

### Updating a Task

1. Select option `4`
2. Enter the task ID
3. Enter the new description

```
Enter your choice: 4
Enter task ID: 1
Enter new description: Buy groceries and milk
✓ Task updated successfully!
```

### Deleting a Task

1. Select option `5`
2. Enter the task ID
3. Confirm deletion

```
Enter your choice: 5
Enter task ID: 1
✓ Task deleted successfully!
```

### Exiting

1. Select option `6`
2. See goodbye message with data loss warning

```
Enter your choice: 6
⚠ Note: All tasks will be lost (in-memory storage only).
Goodbye! Thanks for using Todo App.
```

---

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/unit/test_task_service.py
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

---

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task data model
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # CRUD operations
│   └── cli/
│       ├── __init__.py
│       ├── menu.py          # Menu display
│       └── handlers.py      # Input handlers
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_task_model.py
│   │   └── test_task_service.py
│   └── integration/
│       └── test_cli_flow.py
├── pyproject.toml
└── README.md
```

---

## Troubleshooting

### "Python not found"

Ensure Python 3.13+ is installed and in your PATH:
```bash
python --version
# or
python3 --version
```

### "Module not found" Error

Make sure you've installed in development mode:
```bash
pip install -e .
```

### Ctrl+C Exits Abruptly

The application handles Ctrl+C gracefully. If you see this message, it's working correctly:
```
^C
Goodbye! (interrupted)
```

### Input Not Responding

Ensure your terminal supports standard input. Some IDE integrated terminals may have issues. Try running in a standalone terminal window.

---

## Known Limitations (Phase I)

- **No persistence**: Tasks are lost when the application exits
- **Single user**: No multi-user support
- **No undo**: Deleted tasks cannot be recovered
- **No task priorities or due dates**: These will be added in future phases

---

## Next Steps

After Phase I is complete, Phase II will add:
- Database persistence with Neon DB
- REST API with FastAPI
- Web frontend with Next.js
