# Task Service Contract

**Date**: 2026-01-14
**Feature**: 001-console-todo-app
**Type**: Internal Service API

## Overview

This document defines the contract for the TaskService class, which provides all CRUD operations for todo tasks. This is an internal API (not REST/HTTP) since Phase I is a console application.

---

## Service: TaskService

### Constructor

```python
TaskService()
```

Creates a new TaskService instance with empty task storage.

---

## Operations

### 1. add_task

**Purpose**: Create a new task with the given description.

**Signature**:
```python
def add_task(self, description: str) -> Task
```

**Parameters**:
| Name | Type | Required | Constraints |
|------|------|----------|-------------|
| `description` | str | Yes | 1-500 chars, non-empty |

**Returns**: `Task` - The newly created task with assigned ID

**Behavior**:
- Assigns the next available unique ID
- Sets status to PENDING
- Sets created_at to current timestamp
- Stores the task in memory

**Errors**:
| Condition | Error Type | Message |
|-----------|------------|---------|
| Empty description | `ValueError` | "Description cannot be empty" |
| Description > 500 chars | `ValueError` | "Description exceeds 500 characters" |

---

### 2. get_task

**Purpose**: Retrieve a single task by its ID.

**Signature**:
```python
def get_task(self, task_id: int) -> Task | None
```

**Parameters**:
| Name | Type | Required | Constraints |
|------|------|----------|-------------|
| `task_id` | int | Yes | Positive integer |

**Returns**: `Task | None` - The task if found, None otherwise

**Behavior**:
- Looks up task by ID
- Returns None if not found (does not raise exception)

---

### 3. get_all_tasks

**Purpose**: Retrieve all tasks in the system.

**Signature**:
```python
def get_all_tasks(self) -> list[Task]
```

**Parameters**: None

**Returns**: `list[Task]` - All tasks, may be empty

**Behavior**:
- Returns tasks in creation order (by ID)
- Returns empty list if no tasks exist

---

### 4. update_task

**Purpose**: Update the description of an existing task.

**Signature**:
```python
def update_task(self, task_id: int, new_description: str) -> Task | None
```

**Parameters**:
| Name | Type | Required | Constraints |
|------|------|----------|-------------|
| `task_id` | int | Yes | Positive integer |
| `new_description` | str | Yes | 1-500 chars, non-empty |

**Returns**: `Task | None` - The updated task if found, None if not found

**Behavior**:
- Finds task by ID
- Updates description if found
- Returns None if task not found

**Errors**:
| Condition | Error Type | Message |
|-----------|------------|---------|
| Empty description | `ValueError` | "Description cannot be empty" |
| Description > 500 chars | `ValueError` | "Description exceeds 500 characters" |

---

### 5. delete_task

**Purpose**: Remove a task from the system.

**Signature**:
```python
def delete_task(self, task_id: int) -> bool
```

**Parameters**:
| Name | Type | Required | Constraints |
|------|------|----------|-------------|
| `task_id` | int | Yes | Positive integer |

**Returns**: `bool` - True if task was deleted, False if not found

**Behavior**:
- Removes task from storage if found
- ID is not reused for future tasks
- Returns False if task not found

---

### 6. mark_complete

**Purpose**: Mark a task as completed.

**Signature**:
```python
def mark_complete(self, task_id: int) -> Task | None
```

**Parameters**:
| Name | Type | Required | Constraints |
|------|------|----------|-------------|
| `task_id` | int | Yes | Positive integer |

**Returns**: `Task | None` - The updated task if found, None if not found

**Behavior**:
- Finds task by ID
- Changes status to COMPLETED
- Returns None if task not found
- Idempotent: marking completed task as complete is a no-op (returns task)

---

### 7. get_task_count

**Purpose**: Get the total number of tasks.

**Signature**:
```python
def get_task_count(self) -> int
```

**Parameters**: None

**Returns**: `int` - Total number of tasks (0 or more)

---

## Usage Examples

```python
# Initialize service
service = TaskService()

# Add tasks
task1 = service.add_task("Buy groceries")
task2 = service.add_task("Call mom")

# View all
all_tasks = service.get_all_tasks()
# Returns: [Task(id=1, ...), Task(id=2, ...)]

# Get one
task = service.get_task(1)
# Returns: Task(id=1, description="Buy groceries", ...)

# Update
updated = service.update_task(1, "Buy groceries and milk")
# Returns: Task(id=1, description="Buy groceries and milk", ...)

# Mark complete
completed = service.mark_complete(1)
# Returns: Task(id=1, status=COMPLETED, ...)

# Delete
success = service.delete_task(2)
# Returns: True

# Not found cases
service.get_task(999)       # Returns: None
service.update_task(999, "x")  # Returns: None
service.delete_task(999)    # Returns: False
service.mark_complete(999)  # Returns: None
```

---

## Thread Safety

Phase I assumes single-threaded operation. No locking or synchronization is provided. This will be addressed in Phase II when web server concurrency is introduced.

---

## Migration to REST API (Phase II)

| Service Method | REST Endpoint | HTTP Method |
|----------------|---------------|-------------|
| `add_task` | `/tasks` | POST |
| `get_task` | `/tasks/{id}` | GET |
| `get_all_tasks` | `/tasks` | GET |
| `update_task` | `/tasks/{id}` | PUT |
| `delete_task` | `/tasks/{id}` | DELETE |
| `mark_complete` | `/tasks/{id}/complete` | POST |
