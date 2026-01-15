"""Task service for CRUD operations on todo tasks.

This module provides the TaskService class which handles all business
logic for creating, reading, updating, and deleting tasks. Tasks are
stored in memory for Phase I.
"""

from src.models.task import Task, TaskStatus


class TaskService:
    """Service class for managing todo tasks.

    Provides CRUD operations for tasks stored in memory. Each task is
    assigned a unique ID that is never reused, even after deletion.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects.
        _next_id: The next ID to be assigned to a new task.

    Example:
        >>> service = TaskService()
        >>> task = service.add_task("Buy groceries")
        >>> task.id
        1
        >>> service.get_task_count()
        1
    """

    MAX_DESCRIPTION_LENGTH = 500

    def __init__(self) -> None:
        """Initialize a new TaskService with empty storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, description: str) -> Task:
        """Create a new task with the given description.

        Args:
            description: Text describing what needs to be done.
                Must be between 1 and 500 characters.

        Returns:
            The newly created Task with assigned ID and PENDING status.

        Raises:
            ValueError: If description is empty or exceeds 500 characters.

        Example:
            >>> service = TaskService()
            >>> task = service.add_task("Call mom")
            >>> task.description
            'Call mom'
            >>> task.status
            <TaskStatus.PENDING: 'Pending'>
        """
        self._validate_description(description)

        task = Task(
            id=self._next_id,
            description=description.strip(),
            status=TaskStatus.PENDING,
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Task | None:
        """Retrieve a single task by its ID.

        Args:
            task_id: The unique identifier of the task to retrieve.

        Returns:
            The Task if found, None otherwise.

        Example:
            >>> service = TaskService()
            >>> service.add_task("Test task")
            >>> task = service.get_task(1)
            >>> task.description
            'Test task'
            >>> service.get_task(999) is None
            True
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks in the system.

        Returns:
            List of all tasks in creation order (by ID).
            Returns an empty list if no tasks exist.

        Example:
            >>> service = TaskService()
            >>> service.add_task("Task 1")
            >>> service.add_task("Task 2")
            >>> len(service.get_all_tasks())
            2
        """
        return list(self._tasks.values())

    def get_task_count(self) -> int:
        """Get the total number of tasks.

        Returns:
            The number of tasks currently stored.

        Example:
            >>> service = TaskService()
            >>> service.get_task_count()
            0
            >>> service.add_task("Task")
            >>> service.get_task_count()
            1
        """
        return len(self._tasks)

    def update_task(self, task_id: int, new_description: str) -> Task | None:
        """Update the description of an existing task.

        Args:
            task_id: The unique identifier of the task to update.
            new_description: The new description text.
                Must be between 1 and 500 characters.

        Returns:
            The updated Task if found, None if task not found.

        Raises:
            ValueError: If new_description is empty or exceeds 500 characters.

        Example:
            >>> service = TaskService()
            >>> service.add_task("Buy milk")
            >>> updated = service.update_task(1, "Buy milk and eggs")
            >>> updated.description
            'Buy milk and eggs'
        """
        self._validate_description(new_description)

        task = self._tasks.get(task_id)
        if task is None:
            return None

        task.update_description(new_description.strip())
        return task

    def delete_task(self, task_id: int) -> bool:
        """Remove a task from the system.

        The task's ID will not be reused for future tasks.

        Args:
            task_id: The unique identifier of the task to delete.

        Returns:
            True if the task was deleted, False if not found.

        Example:
            >>> service = TaskService()
            >>> service.add_task("Task to delete")
            >>> service.delete_task(1)
            True
            >>> service.delete_task(1)
            False
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def mark_complete(self, task_id: int) -> Task | None:
        """Mark a task as completed.

        This is an idempotent operation - marking an already completed
        task as complete will return the task without error.

        Args:
            task_id: The unique identifier of the task to complete.

        Returns:
            The updated Task if found, None if not found.

        Example:
            >>> service = TaskService()
            >>> service.add_task("Complete me")
            >>> task = service.mark_complete(1)
            >>> task.is_completed()
            True
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        task.mark_complete()
        return task

    def _validate_description(self, description: str) -> None:
        """Validate a task description.

        Args:
            description: The description to validate.

        Raises:
            ValueError: If description is empty, whitespace-only,
                or exceeds the maximum length.
        """
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")
        if len(description.strip()) > self.MAX_DESCRIPTION_LENGTH:
            raise ValueError(
                f"Description exceeds {self.MAX_DESCRIPTION_LENGTH} characters"
            )
