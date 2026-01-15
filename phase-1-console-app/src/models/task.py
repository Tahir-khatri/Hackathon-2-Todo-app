"""Task model for the Todo application.

This module defines the Task entity and TaskStatus enum used throughout
the application to represent todo items.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Possible states for a task.

    Attributes:
        PENDING: Task has not been completed yet.
        COMPLETED: Task has been marked as done.
    """

    PENDING = "Pending"
    COMPLETED = "Completed"


@dataclass
class Task:
    """Represents a todo item.

    A task is a single unit of work that a user wants to track. Each task
    has a unique ID assigned by the system, a description of what needs
    to be done, a status indicating whether it's pending or completed,
    and a timestamp of when it was created.

    Attributes:
        id: Unique numeric identifier assigned by the system.
        description: Text describing what needs to be done (1-500 characters).
        status: Current state of the task (Pending or Completed).
        created_at: Timestamp when the task was created.

    Example:
        >>> task = Task(id=1, description="Buy groceries")
        >>> task.status
        <TaskStatus.PENDING: 'Pending'>
        >>> task.mark_complete()
        >>> task.status
        <TaskStatus.COMPLETED: 'Completed'>
    """

    id: int
    description: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)

    def mark_complete(self) -> None:
        """Mark this task as completed.

        Changes the task status from PENDING to COMPLETED.
        This is an idempotent operation - calling it on an already
        completed task has no effect.
        """
        self.status = TaskStatus.COMPLETED

    def update_description(self, new_description: str) -> None:
        """Update the task description.

        Args:
            new_description: The new description text for the task.
        """
        self.description = new_description

    def is_completed(self) -> bool:
        """Check if the task is completed.

        Returns:
            True if the task status is COMPLETED, False otherwise.
        """
        return self.status == TaskStatus.COMPLETED

    def __str__(self) -> str:
        """Return a human-readable string representation of the task.

        Returns:
            A formatted string showing the task's status indicator,
            ID, and description.
        """
        status_indicator = "[x]" if self.is_completed() else "[ ]"
        return f"{status_indicator} {self.id}. {self.description}"
