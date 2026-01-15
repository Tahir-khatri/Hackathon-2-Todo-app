# Data Model: In-Memory Python Console Todo App (Phase I)

**Date**: 2026-01-14
**Feature**: 001-console-todo-app

## Overview

This document defines the data entities, their attributes, relationships, and validation rules for Phase I of the todo application. The model is designed for in-memory storage while maintaining compatibility with future database persistence in Phase II.

---

## Entities

### Task

**Purpose**: Represents a single todo item that a user wants to track.

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `id` | int | Yes | Auto-generated | Positive integer, unique | System-assigned identifier |
| `description` | str | Yes | - | 1-500 characters, non-empty | What needs to be done |
| `status` | TaskStatus | Yes | PENDING | PENDING or COMPLETED | Current state of the task |
| `created_at` | datetime | No | Current time | Valid datetime | When task was created (future use) |

### TaskStatus (Enum)

**Purpose**: Defines the possible states of a task.

| Value | Display String | Description |
|-------|----------------|-------------|
| `PENDING` | "Pending" | Task has not been completed |
| `COMPLETED` | "Completed" | Task has been marked as done |

---

## Validation Rules

### Task ID
- MUST be a positive integer (> 0)
- MUST be unique within the session
- MUST NOT be reused after task deletion

### Task Description
- MUST contain at least 1 character after trimming whitespace
- MUST NOT exceed 500 characters
- MUST NOT be empty or whitespace-only

### Task Status
- MUST be one of: PENDING, COMPLETED
- New tasks MUST default to PENDING
- Status changes are one-way: PENDING → COMPLETED

---

## State Transitions

```
┌─────────────────┐
│                 │
│    [Created]    │
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│                 │
│    PENDING      │ ◄── Initial state for all new tasks
│                 │
└────────┬────────┘
         │
         │ mark_complete()
         ▼
┌─────────────────┐
│                 │
│   COMPLETED     │ ◄── Terminal state (cannot revert in Phase I)
│                 │
└─────────────────┘
```

**Note**: In Phase I, there is no transition from COMPLETED back to PENDING. This simplification aligns with the beginner-focused scope. Future phases may add an "uncomplete" feature.

---

## Storage Model

### In-Memory Structure

```python
# Primary storage: dict keyed by task ID
_tasks: dict[int, Task] = {
    1: Task(id=1, description="Buy groceries", status=TaskStatus.PENDING),
    2: Task(id=2, description="Call mom", status=TaskStatus.COMPLETED),
}

# ID counter: simple incrementing integer
_next_id: int = 3
```

### Operations Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Add task | O(1) | O(1) |
| Get task by ID | O(1) | O(1) |
| Get all tasks | O(n) | O(n) |
| Update task | O(1) | O(1) |
| Delete task | O(1) | O(1) |
| Mark complete | O(1) | O(1) |

---

## Python Implementation Reference

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    """Possible states for a task."""
    PENDING = "Pending"
    COMPLETED = "Completed"


@dataclass
class Task:
    """
    Represents a todo item.

    Attributes:
        id: Unique identifier assigned by the system
        description: Text describing what needs to be done
        status: Current state (Pending or Completed)
        created_at: Timestamp when task was created
    """
    id: int
    description: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.status = TaskStatus.COMPLETED

    def update_description(self, new_description: str) -> None:
        """Update the task description."""
        self.description = new_description

    def is_completed(self) -> bool:
        """Check if the task is completed."""
        return self.status == TaskStatus.COMPLETED
```

---

## Migration Path to Phase II

When adding database persistence in Phase II, the Task entity will be extended:

| Phase I | Phase II Addition |
|---------|-------------------|
| `id: int` | Becomes primary key in database |
| `description: str` | Maps to VARCHAR(500) |
| `status: TaskStatus` | Maps to ENUM column |
| `created_at: datetime` | Maps to TIMESTAMP with default |
| - | `updated_at: datetime` (new field) |
| - | `user_id: int` (foreign key for multi-user) |

The in-memory `dict[int, Task]` will be replaced by SQLModel ORM operations, but the Task class interface remains stable.

---

## Relationships

Phase I has a single entity (Task) with no relationships. Future phases will introduce:

- **Phase II**: User → Task (one-to-many)
- **Phase III**: Task → AIConversation (one-to-many for AI interactions)
