"""Unit tests for the TaskService.

Tests cover all CRUD operations and validation logic.
"""

import pytest

from src.models.task import TaskStatus
from src.services.task_service import TaskService


@pytest.fixture
def service():
    """Create a fresh TaskService for each test."""
    return TaskService()


class TestAddTask:
    """Tests for TaskService.add_task()."""

    def test_add_task_returns_task_with_id(self, service):
        """add_task() returns a Task with an assigned ID."""
        task = service.add_task("Buy groceries")

        assert task.id == 1
        assert task.description == "Buy groceries"

    def test_add_task_assigns_sequential_ids(self, service):
        """Each new task gets the next sequential ID."""
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_sets_pending_status(self, service):
        """New tasks have PENDING status."""
        task = service.add_task("New task")

        assert task.status == TaskStatus.PENDING

    def test_add_task_trims_whitespace(self, service):
        """Description whitespace is trimmed."""
        task = service.add_task("  Trim me  ")

        assert task.description == "Trim me"

    def test_add_task_empty_description_raises_error(self, service):
        """Empty description raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.add_task("")

    def test_add_task_whitespace_only_raises_error(self, service):
        """Whitespace-only description raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.add_task("   ")

    def test_add_task_exceeds_max_length_raises_error(self, service):
        """Description over 500 chars raises ValueError."""
        long_description = "a" * 501
        with pytest.raises(ValueError, match="exceeds 500 characters"):
            service.add_task(long_description)

    def test_add_task_at_max_length_succeeds(self, service):
        """Description at exactly 500 chars succeeds."""
        description = "a" * 500
        task = service.add_task(description)

        assert len(task.description) == 500


class TestGetTask:
    """Tests for TaskService.get_task()."""

    def test_get_task_returns_task_by_id(self, service):
        """get_task() returns the task with matching ID."""
        service.add_task("Task 1")
        task2 = service.add_task("Task 2")

        result = service.get_task(2)

        assert result == task2
        assert result.description == "Task 2"

    def test_get_task_not_found_returns_none(self, service):
        """get_task() returns None for non-existent ID."""
        result = service.get_task(999)

        assert result is None

    def test_get_task_after_deletion_returns_none(self, service):
        """get_task() returns None for deleted task."""
        service.add_task("Task to delete")
        service.delete_task(1)

        result = service.get_task(1)

        assert result is None


class TestGetAllTasks:
    """Tests for TaskService.get_all_tasks()."""

    def test_get_all_tasks_empty_service(self, service):
        """get_all_tasks() returns empty list when no tasks."""
        result = service.get_all_tasks()

        assert result == []

    def test_get_all_tasks_returns_all_tasks(self, service):
        """get_all_tasks() returns all stored tasks."""
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        result = service.get_all_tasks()

        assert len(result) == 3
        assert [t.description for t in result] == ["Task 1", "Task 2", "Task 3"]

    def test_get_all_tasks_in_creation_order(self, service):
        """Tasks are returned in creation order."""
        service.add_task("First")
        service.add_task("Second")
        service.add_task("Third")

        result = service.get_all_tasks()

        assert result[0].id == 1
        assert result[1].id == 2
        assert result[2].id == 3


class TestGetTaskCount:
    """Tests for TaskService.get_task_count()."""

    def test_get_task_count_empty_service(self, service):
        """get_task_count() returns 0 when no tasks."""
        assert service.get_task_count() == 0

    def test_get_task_count_after_adding(self, service):
        """get_task_count() returns correct count after adding."""
        service.add_task("Task 1")
        service.add_task("Task 2")

        assert service.get_task_count() == 2

    def test_get_task_count_after_deletion(self, service):
        """get_task_count() reflects deletions."""
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.delete_task(1)

        assert service.get_task_count() == 1


class TestUpdateTask:
    """Tests for TaskService.update_task()."""

    def test_update_task_changes_description(self, service):
        """update_task() changes the task description."""
        service.add_task("Old description")

        result = service.update_task(1, "New description")

        assert result.description == "New description"

    def test_update_task_not_found_returns_none(self, service):
        """update_task() returns None for non-existent ID."""
        result = service.update_task(999, "New description")

        assert result is None

    def test_update_task_empty_description_raises_error(self, service):
        """update_task() with empty description raises ValueError."""
        service.add_task("Task")

        with pytest.raises(ValueError, match="cannot be empty"):
            service.update_task(1, "")

    def test_update_task_trims_whitespace(self, service):
        """update_task() trims whitespace from description."""
        service.add_task("Original")

        result = service.update_task(1, "  Updated  ")

        assert result.description == "Updated"


class TestDeleteTask:
    """Tests for TaskService.delete_task()."""

    def test_delete_task_removes_task(self, service):
        """delete_task() removes the task from storage."""
        service.add_task("Task to delete")

        result = service.delete_task(1)

        assert result is True
        assert service.get_task(1) is None

    def test_delete_task_not_found_returns_false(self, service):
        """delete_task() returns False for non-existent ID."""
        result = service.delete_task(999)

        assert result is False

    def test_delete_task_id_not_reused(self, service):
        """Deleted task IDs are not reused."""
        service.add_task("Task 1")
        service.delete_task(1)
        task2 = service.add_task("Task 2")

        assert task2.id == 2  # Not 1


class TestMarkComplete:
    """Tests for TaskService.mark_complete()."""

    def test_mark_complete_changes_status(self, service):
        """mark_complete() changes task status to COMPLETED."""
        service.add_task("Task to complete")

        result = service.mark_complete(1)

        assert result.status == TaskStatus.COMPLETED
        assert result.is_completed()

    def test_mark_complete_not_found_returns_none(self, service):
        """mark_complete() returns None for non-existent ID."""
        result = service.mark_complete(999)

        assert result is None

    def test_mark_complete_already_completed(self, service):
        """mark_complete() on completed task returns the task."""
        service.add_task("Task")
        service.mark_complete(1)

        result = service.mark_complete(1)

        assert result is not None
        assert result.is_completed()
