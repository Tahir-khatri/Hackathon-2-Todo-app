# Todo Console App - Phase I

A simple in-memory Python console application for managing todo tasks. This is Phase I of the multi-phase Todo Application project.

## Features

- **Add Task**: Create new tasks with descriptions
- **View All Tasks**: See all tasks with their status (pending/completed)
- **Mark Complete**: Mark tasks as done
- **Update Task**: Edit task descriptions
- **Delete Task**: Remove tasks from the list
- **Graceful Exit**: Exit with data loss warning

## Prerequisites

- Python 3.11+ (Python 3.13+ recommended)
- pip (for installing dependencies)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hackathon-2-evolution-of-todo
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

Or if installed:

```bash
todo
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
✓ Task added successfully! (ID: 1)

========== Todo App ==========
...
Enter your choice: 2

========== Your Tasks ==========
[ ] 1. Buy groceries
================================
Total: 1 task (1 pending, 0 completed)
```

## Running Tests

Install pytest if not already installed:

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

Run specific test files:

```bash
pytest tests/unit/test_task_model.py
pytest tests/unit/test_task_service.py
pytest tests/integration/test_cli_flow.py
```

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task data model
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
├── specs/                   # Feature specifications
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Limitations (Phase I)

- **No persistence**: Tasks are stored in memory only and are lost when the application exits
- **Single user**: No multi-user support
- **No undo**: Deleted tasks cannot be recovered
- **Console only**: No web interface or API

## Next Phases

- **Phase II**: Web application with database persistence (FastAPI + Next.js + Neon DB)
- **Phase III**: AI-powered chatbot integration
- **Phase IV**: Local Kubernetes deployment
- **Phase V**: Cloud deployment with event-driven architecture

## License

MIT License
