"""Unit tests for the Task model.

Tests cover Task creation, status changes, and string representation.
"""

import pytest
from datetime import datetime

from src.models.task import Task, TaskStatus


class TestTaskStatus:
    """Tests for the TaskStatus enum."""

    def test_pending_value(self):
        """PENDING status has correct display value."""
        assert TaskStatus.PENDING.value == "Pending"

    def test_completed_value(self):
        """COMPLETED status has correct display value."""
        assert TaskStatus.COMPLETED.value == "Completed"


class TestTaskCreation:
    """Tests for Task creation and initialization."""

    def test_create_task_with_required_fields(self):
        """Task can be created with just id and description."""
        task = Task(id=1, description="Test task")

        assert task.id == 1
        assert task.description == "Test task"
        assert task.status == TaskStatus.PENDING
        assert isinstance(task.created_at, datetime)

    def test_create_task_with_custom_status(self):
        """Task can be created with a custom status."""
        task = Task(id=2, description="Completed task", status=TaskStatus.COMPLETED)

        assert task.status == TaskStatus.COMPLETED

    def test_task_default_status_is_pending(self):
        """New tasks default to PENDING status."""
        task = Task(id=1, description="New task")

        assert task.status == TaskStatus.PENDING
        assert not task.is_completed()


class TestTaskMethods:
    """Tests for Task instance methods."""

    def test_mark_complete_changes_status(self):
        """mark_complete() changes status to COMPLETED."""
        task = Task(id=1, description="Task to complete")

        task.mark_complete()

        assert task.status == TaskStatus.COMPLETED
        assert task.is_completed()

    def test_mark_complete_is_idempotent(self):
        """Calling mark_complete() multiple times has same result."""
        task = Task(id=1, description="Task")
        task.mark_complete()
        task.mark_complete()

        assert task.status == TaskStatus.COMPLETED

    def test_update_description(self):
        """update_description() changes the task description."""
        task = Task(id=1, description="Old description")

        task.update_description("New description")

        assert task.description == "New description"

    def test_is_completed_returns_false_for_pending(self):
        """is_completed() returns False for PENDING tasks."""
        task = Task(id=1, description="Pending task")

        assert not task.is_completed()

    def test_is_completed_returns_true_for_completed(self):
        """is_completed() returns True for COMPLETED tasks."""
        task = Task(id=1, description="Done task", status=TaskStatus.COMPLETED)

        assert task.is_completed()


class TestTaskStringRepresentation:
    """Tests for Task string representation."""

    def test_str_pending_task(self):
        """Pending task shows [ ] indicator."""
        task = Task(id=1, description="Buy groceries")

        result = str(task)

        assert result == "[ ] 1. Buy groceries"

    def test_str_completed_task(self):
        """Completed task shows [x] indicator."""
        task = Task(id=2, description="Call mom", status=TaskStatus.COMPLETED)

        result = str(task)

        assert result == "[x] 2. Call mom"
