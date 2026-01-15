# Phase 1: Console Todo App

A simple in-memory Python console application for managing todo tasks. This is **Phase 1** of the Multi-phase Todo Application project.

## Overview

Phase 1 implements a command-line todo application with full CRUD (Create, Read, Update, Delete) operations. All data is stored in-memory and will be lost when the application exits.

## Features

| Feature | Description |
|---------|-------------|
| **Add Task** | Create new tasks with descriptions (1-500 characters) |
| **View All Tasks** | See all tasks with status indicators `[ ]` pending / `[x]` completed |
| **Mark Complete** | Mark tasks as done by ID |
| **Update Task** | Edit task descriptions |
| **Delete Task** | Remove tasks from the list |
| **Graceful Exit** | Exit with data loss warning |

## Prerequisites

- Python 3.11 or higher (Python 3.13+ recommended)
- pip (for installing dependencies)

## Installation

1. Navigate to the phase-1-console-app directory:
   ```bash
   cd phase-1-console-app
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   ```

## Usage

Run the application:

```bash
python -m src.main
```

### Menu Options

```
========== Todo App ==========
1. Add Task
2. View All Tasks
3. Mark Task Complete
4. Update Task
5. Delete Task
6. Exit
==============================
```

### Example Session

```
Welcome to Todo App!
A simple in-memory task manager.

========== Todo App ==========
1. Add Task
2. View All Tasks
3. Mark Task Complete
4. Update Task
5. Delete Task
6. Exit
==============================
Enter your choice: 1

--- Add New Task ---
Enter task description: Buy groceries
[OK] Task added successfully! (ID: 1)

========== Todo App ==========
...
Enter your choice: 2

========== Your Tasks ==========
[ ] 1. Buy groceries
================================
Total: 1 task (1 pending, 0 completed)

Enter your choice: 3

--- Mark Task Complete ---
Enter task ID: 1
[OK] Task marked as complete!

Enter your choice: 2

========== Your Tasks ==========
[x] 1. Buy groceries
================================
Total: 1 task (0 pending, 1 completed)
```

## Running Tests

Install pytest (if not already installed):

```bash
pip install pytest
```

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

### Test Coverage

| Test File | Tests | Description |
|-----------|-------|-------------|
| `tests/unit/test_task_model.py` | 12 | Task dataclass and enum tests |
| `tests/unit/test_task_service.py` | 27 | CRUD operations and validation |
| `tests/integration/test_cli_flow.py` | 11 | End-to-end CLI workflows |
| **Total** | **50** | All passing |

## Project Structure

```
phase-1-console-app/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task data model & TaskStatus enum
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # CRUD business logic
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
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

## Architecture

### Components

1. **Task Model** (`src/models/task.py`)
   - `TaskStatus` enum: PENDING, COMPLETED
   - `Task` dataclass: id, description, status, created_at

2. **Task Service** (`src/services/task_service.py`)
   - In-memory storage using Python dict
   - Sequential ID assignment (never reused)
   - Validation: 1-500 character descriptions

3. **CLI Handlers** (`src/cli/handlers.py`)
   - One handler per menu option
   - Input validation with helpful error messages

4. **Main Loop** (`src/main.py`)
   - Menu-driven interface
   - Keyboard interrupt handling (Ctrl+C)

## Limitations (Phase 1)

| Limitation | Description |
|------------|-------------|
| No Persistence | Tasks stored in memory only - lost on exit |
| Single User | No multi-user or concurrent access support |
| No Undo | Deleted tasks cannot be recovered |
| Console Only | No web interface, API, or GUI |

## What's Next?

This Phase 1 console app serves as the foundation for future phases:

| Phase | Description |
|-------|-------------|
| Phase 2 | Web application with database persistence (FastAPI + Next.js + Neon DB) |
| Phase 3 | AI-powered chatbot integration |
| Phase 4 | Local Kubernetes deployment |
| Phase 5 | Cloud deployment with event-driven architecture |

## License

MIT License
