# Research: In-Memory Python Console Todo App (Phase I)

**Date**: 2026-01-14
**Feature**: 001-console-todo-app

## Research Summary

This document captures technical decisions and best practices research for Phase I of the todo application. Since this phase uses only Python standard library, research focuses on patterns and practices rather than library selection.

---

## 1. Python Console Input Handling

### Decision
Use `input()` with try/except for Ctrl+C handling via `KeyboardInterrupt`.

### Rationale
- `input()` is the standard way to read user input in Python
- `KeyboardInterrupt` provides clean signal handling without external libraries
- Beginner-friendly approach that's easy to understand and debug

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| `sys.stdin.readline()` | Lower-level, less beginner-friendly |
| `curses` library | Overkill for simple menu; not cross-platform on Windows |
| `rich` or `prompt_toolkit` | External dependencies; not allowed in Phase I |

### Implementation Pattern
```python
def get_user_input(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        raise SystemExit(0)
```

---

## 2. Task ID Generation Strategy

### Decision
Use a simple incrementing integer counter stored as a class attribute.

### Rationale
- Guarantees uniqueness within a session
- Simple to implement and understand
- IDs remain stable (no reassignment after deletion)
- Efficient O(1) ID generation

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| UUID | Overkill for in-memory; harder for users to type |
| Reuse deleted IDs | Confusing; "Task 3" might refer to different tasks over time |
| Timestamp-based | Millisecond resolution not needed; harder to type |

### Implementation Pattern
```python
class TaskService:
    _next_id: int = 1

    def create_task(self, description: str) -> Task:
        task = Task(id=self._next_id, description=description)
        self._next_id += 1
        return task
```

---

## 3. In-Memory Storage Structure

### Decision
Use a Python `dict` keyed by task ID for O(1) lookups, with list comprehension for iteration.

### Rationale
- O(1) lookup by ID for update/delete/complete operations
- Easy iteration for view all
- Memory efficient for expected scale (100 tasks)
- Preserves insertion order (Python 3.7+)

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Plain list | O(n) lookup by ID |
| SQLite in-memory | External dependency feel; overkill |
| dataclasses dict | Same as dict; dataclass for Task entity is fine |

### Implementation Pattern
```python
class TaskService:
    def __init__(self):
        self._tasks: dict[int, Task] = {}

    def get_task(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        return list(self._tasks.values())
```

---

## 4. Task Data Model Design

### Decision
Use Python `dataclass` for the Task entity with explicit types.

### Rationale
- Built into Python standard library (no dependencies)
- Provides automatic `__init__`, `__repr__`, `__eq__`
- Clear, self-documenting structure
- Easy to extend with additional fields in future phases

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Plain dict | No type hints, easy to misspell keys |
| NamedTuple | Immutable; we need to update status |
| Pydantic | External dependency |

### Implementation Pattern
```python
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

@dataclass
class Task:
    id: int
    description: str
    status: TaskStatus = TaskStatus.PENDING
```

---

## 5. Input Validation Strategy

### Decision
Validate at the CLI handler layer before passing to service layer.

### Rationale
- Separation of concerns: CLI handles user interaction, service handles business logic
- Service layer can assume valid inputs (cleaner code)
- Error messages are context-aware (knows about menu state)
- Easier to test service layer in isolation

### Validation Rules
| Input | Validation | Error Message |
|-------|------------|---------------|
| Task ID | Must be positive integer | "Invalid input. Please enter a number." |
| Description | 1-500 chars, not whitespace-only | "Description cannot be empty." |
| Menu choice | Must be valid option number | "Invalid choice. Please try again." |

### Implementation Pattern
```python
def get_task_id() -> int | None:
    raw = get_user_input("Enter task ID: ")
    try:
        task_id = int(raw)
        if task_id <= 0:
            print("Invalid ID. Please enter a positive number.")
            return None
        return task_id
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None
```

---

## 6. CLI Menu Design Pattern

### Decision
Use a numbered menu with a main loop dispatching to handlers.

### Rationale
- Familiar pattern for CLI applications
- Easy to extend with new options
- Clear mapping from user choice to action
- Supports both number and potentially keyword shortcuts

### Menu Layout
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

### Implementation Pattern
```python
MENU_OPTIONS = {
    "1": ("Add Task", handle_add_task),
    "2": ("View All Tasks", handle_view_tasks),
    "3": ("Mark Task Complete", handle_mark_complete),
    "4": ("Update Task", handle_update_task),
    "5": ("Delete Task", handle_delete_task),
    "6": ("Exit", handle_exit),
}

def main_loop(service: TaskService):
    while True:
        display_menu()
        choice = get_user_input("Enter your choice: ")
        if choice in MENU_OPTIONS:
            _, handler = MENU_OPTIONS[choice]
            handler(service)
        else:
            print("Invalid choice. Please try again.")
```

---

## 7. Testing Strategy

### Decision
Use pytest with fixtures for service instances; test CLI handlers with monkeypatch for input/output.

### Rationale
- pytest is the de facto Python testing standard
- Fixtures provide clean test isolation
- monkeypatch enables testing of input/output without subprocess

### Test Categories
| Category | What to Test | Example |
|----------|--------------|---------|
| Unit: Task model | Creation, status change | `test_task_creation()` |
| Unit: TaskService | CRUD operations | `test_add_task()`, `test_delete_task()` |
| Integration: CLI | Full user flows | `test_add_and_view_task()` |

### Implementation Pattern
```python
import pytest
from src.services.task_service import TaskService

@pytest.fixture
def service():
    return TaskService()

def test_add_task(service):
    task = service.add_task("Buy groceries")
    assert task.id == 1
    assert task.description == "Buy groceries"
    assert task.status == TaskStatus.PENDING
```

---

## Resolved Clarifications

No NEEDS CLARIFICATION items were identified in the Technical Context. All decisions were made based on:
- Constitution requirements (Phase I constraints)
- Feature specification (14 functional requirements)
- Best practices for beginner-friendly Python code

---

## Next Steps

1. Proceed to Phase 1: Generate data-model.md with entity definitions
2. Generate contracts/ with internal service API definitions
3. Generate quickstart.md with setup and usage instructions
