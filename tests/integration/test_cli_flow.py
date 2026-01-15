"""Integration tests for the CLI flow.

Tests verify that the complete user journey works end-to-end.
"""

import pytest
from io import StringIO
from unittest.mock import patch

from src.services.task_service import TaskService
from src.cli.handlers import (
    handle_add_task,
    handle_view_tasks,
    handle_mark_complete,
    handle_update_task,
    handle_delete_task,
)


@pytest.fixture
def service():
    """Create a fresh TaskService for each test."""
    return TaskService()


class TestAddAndViewFlow:
    """Test the add task and view tasks flow."""

    def test_add_single_task_and_view(self, service, capsys):
        """User can add a task and see it in the list."""
        # Add a task
        with patch("builtins.input", return_value="Buy groceries"):
            handle_add_task(service)

        captured = capsys.readouterr()
        assert "[OK] Task added successfully" in captured.out
        assert "ID: 1" in captured.out

        # View tasks
        handle_view_tasks(service)

        captured = capsys.readouterr()
        assert "[ ] 1. Buy groceries" in captured.out
        assert "1 task" in captured.out

    def test_add_multiple_tasks_and_view(self, service, capsys):
        """User can add multiple tasks and see them all."""
        tasks = ["Task 1", "Task 2", "Task 3"]

        for task in tasks:
            with patch("builtins.input", return_value=task):
                handle_add_task(service)

        handle_view_tasks(service)

        captured = capsys.readouterr()
        assert "[ ] 1. Task 1" in captured.out
        assert "[ ] 2. Task 2" in captured.out
        assert "[ ] 3. Task 3" in captured.out
        assert "3 tasks" in captured.out


class TestCompleteTaskFlow:
    """Test the mark complete flow."""

    def test_add_and_complete_task(self, service, capsys):
        """User can add a task and mark it complete."""
        # Add task
        with patch("builtins.input", return_value="Complete me"):
            handle_add_task(service)

        # Mark complete
        with patch("builtins.input", return_value="1"):
            handle_mark_complete(service)

        captured = capsys.readouterr()
        assert "[OK] Task marked as complete" in captured.out

        # Verify in view
        handle_view_tasks(service)

        captured = capsys.readouterr()
        assert "[x] 1. Complete me" in captured.out
        assert "1 completed" in captured.out

    def test_complete_nonexistent_task(self, service, capsys):
        """Error is shown for non-existent task ID."""
        with patch("builtins.input", return_value="999"):
            handle_mark_complete(service)

        captured = capsys.readouterr()
        assert "Task not found" in captured.out


class TestUpdateTaskFlow:
    """Test the update task flow."""

    def test_add_and_update_task(self, service, capsys):
        """User can add a task and update its description."""
        # Add task
        with patch("builtins.input", return_value="Old description"):
            handle_add_task(service)

        # Update task
        with patch("builtins.input", side_effect=["1", "New description"]):
            handle_update_task(service)

        captured = capsys.readouterr()
        assert "[OK] Task updated successfully" in captured.out

        # Verify in view
        handle_view_tasks(service)

        captured = capsys.readouterr()
        assert "New description" in captured.out
        assert "Old description" not in captured.out


class TestDeleteTaskFlow:
    """Test the delete task flow."""

    def test_add_and_delete_task(self, service, capsys):
        """User can add a task and delete it."""
        # Add task
        with patch("builtins.input", return_value="Delete me"):
            handle_add_task(service)

        # Verify it exists
        handle_view_tasks(service)
        captured = capsys.readouterr()
        assert "Delete me" in captured.out

        # Delete task
        with patch("builtins.input", return_value="1"):
            handle_delete_task(service)

        captured = capsys.readouterr()
        assert "[OK] Task deleted successfully" in captured.out

        # Verify it's gone
        handle_view_tasks(service)

        captured = capsys.readouterr()
        assert "Delete me" not in captured.out
        assert "No tasks yet" in captured.out


class TestEmptyStateFlow:
    """Test flows with empty state."""

    def test_view_empty_list(self, service, capsys):
        """Viewing empty list shows helpful message."""
        handle_view_tasks(service)

        captured = capsys.readouterr()
        assert "No tasks yet" in captured.out
        assert "Add one to get started" in captured.out


class TestValidationFlow:
    """Test input validation in the flow."""

    def test_add_empty_task_rejected(self, service, capsys):
        """Empty task description is rejected."""
        with patch("builtins.input", return_value=""):
            handle_add_task(service)

        captured = capsys.readouterr()
        assert "cannot be empty" in captured.out

        # Verify no task was added
        assert service.get_task_count() == 0

    def test_invalid_task_id_rejected(self, service, capsys):
        """Non-numeric task ID is rejected."""
        with patch("builtins.input", return_value="abc"):
            handle_mark_complete(service)

        captured = capsys.readouterr()
        assert "Please enter a number" in captured.out

    def test_negative_task_id_rejected(self, service, capsys):
        """Negative task ID is rejected."""
        with patch("builtins.input", return_value="-1"):
            handle_mark_complete(service)

        captured = capsys.readouterr()
        assert "positive number" in captured.out


class TestFullCRUDFlow:
    """Test complete CRUD cycle."""

    def test_full_task_lifecycle(self, service, capsys):
        """Test adding, viewing, updating, completing, and deleting a task."""
        # Create
        with patch("builtins.input", return_value="Initial task"):
            handle_add_task(service)
        assert service.get_task_count() == 1

        # Read
        task = service.get_task(1)
        assert task.description == "Initial task"
        assert not task.is_completed()

        # Update
        with patch("builtins.input", side_effect=["1", "Updated task"]):
            handle_update_task(service)
        task = service.get_task(1)
        assert task.description == "Updated task"

        # Complete
        with patch("builtins.input", return_value="1"):
            handle_mark_complete(service)
        task = service.get_task(1)
        assert task.is_completed()

        # Delete
        with patch("builtins.input", return_value="1"):
            handle_delete_task(service)
        assert service.get_task_count() == 0
        assert service.get_task(1) is None
