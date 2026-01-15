"""CLI input handlers for the Todo application.

This module provides functions for handling user input and executing
menu operations. Each handler corresponds to a menu option.
"""

from src.services.task_service import TaskService


def get_user_input(prompt: str) -> str:
    """Get input from the user with KeyboardInterrupt handling.

    Args:
        prompt: The prompt to display to the user.

    Returns:
        The user's input, stripped of leading/trailing whitespace.

    Raises:
        SystemExit: If the user presses Ctrl+C.

    Example:
        >>> # When user types "hello"
        >>> get_user_input("Enter text: ")
        'hello'
    """
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\n\nGoodbye! (interrupted)")
        raise SystemExit(0)


def get_task_id(prompt: str = "Enter task ID: ") -> int | None:
    """Get a valid task ID from the user.

    Prompts the user for a task ID and validates that it is a positive integer.

    Args:
        prompt: The prompt to display to the user.

    Returns:
        The task ID as an integer if valid, None if invalid.

    Example:
        >>> # When user types "5"
        >>> get_task_id()
        5
        >>> # When user types "abc"
        >>> get_task_id()  # Prints error message
        None
    """
    raw = get_user_input(prompt)
    try:
        task_id = int(raw)
        if task_id <= 0:
            print("Invalid ID. Please enter a positive number.")
            return None
        return task_id
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def handle_add_task(service: TaskService) -> None:
    """Handle the Add Task menu option.

    Prompts the user for a task description and creates a new task.

    Args:
        service: The TaskService instance to use for creating the task.

    Example:
        >>> service = TaskService()
        >>> handle_add_task(service)  # User enters "Buy groceries"
        [OK] Task added successfully! (ID: 1)
    """
    print("\n--- Add New Task ---")
    description = get_user_input("Enter task description: ")

    if not description:
        print("Error: Description cannot be empty.")
        return

    try:
        task = service.add_task(description)
        print(f"[OK] Task added successfully! (ID: {task.id})")
    except ValueError as e:
        print(f"Error: {e}")


def handle_view_tasks(service: TaskService) -> None:
    """Handle the View All Tasks menu option.

    Displays all tasks with their ID, status, and description.

    Args:
        service: The TaskService instance to use for retrieving tasks.

    Example:
        >>> service = TaskService()
        >>> service.add_task("Task 1")
        >>> handle_view_tasks(service)
        ========== Your Tasks ==========
        [ ] 1. Task 1
        ================================
        Total: 1 task (1 pending, 0 completed)
    """
    print("\n========== Your Tasks ==========")

    tasks = service.get_all_tasks()

    if not tasks:
        print("No tasks yet. Add one to get started!")
        print("================================")
        return

    for task in tasks:
        print(task)

    print("================================")

    # Show summary
    total = len(tasks)
    completed = sum(1 for t in tasks if t.is_completed())
    pending = total - completed

    task_word = "task" if total == 1 else "tasks"
    print(f"Total: {total} {task_word} ({pending} pending, {completed} completed)")


def handle_mark_complete(service: TaskService) -> None:
    """Handle the Mark Task Complete menu option.

    Prompts for a task ID and marks that task as completed.

    Args:
        service: The TaskService instance to use.

    Example:
        >>> service = TaskService()
        >>> service.add_task("Task to complete")
        >>> handle_mark_complete(service)  # User enters "1"
        [OK] Task marked as complete!
    """
    print("\n--- Mark Task Complete ---")

    task_id = get_task_id()
    if task_id is None:
        return

    task = service.get_task(task_id)
    if task is None:
        print("Error: Task not found.")
        return

    if task.is_completed():
        print("This task is already completed.")
        return

    service.mark_complete(task_id)
    print("[OK] Task marked as complete!")


def handle_update_task(service: TaskService) -> None:
    """Handle the Update Task menu option.

    Prompts for a task ID and new description, then updates the task.

    Args:
        service: The TaskService instance to use.

    Example:
        >>> service = TaskService()
        >>> service.add_task("Old description")
        >>> handle_update_task(service)  # User enters "1" then "New description"
        [OK] Task updated successfully!
    """
    print("\n--- Update Task ---")

    task_id = get_task_id()
    if task_id is None:
        return

    task = service.get_task(task_id)
    if task is None:
        print("Error: Task not found.")
        return

    print(f"Current description: {task.description}")
    new_description = get_user_input("Enter new description: ")

    if not new_description:
        print("Error: Description cannot be empty.")
        return

    try:
        service.update_task(task_id, new_description)
        print("[OK] Task updated successfully!")
    except ValueError as e:
        print(f"Error: {e}")


def handle_delete_task(service: TaskService) -> None:
    """Handle the Delete Task menu option.

    Prompts for a task ID and deletes that task.

    Args:
        service: The TaskService instance to use.

    Example:
        >>> service = TaskService()
        >>> service.add_task("Task to delete")
        >>> handle_delete_task(service)  # User enters "1"
        [OK] Task deleted successfully!
    """
    print("\n--- Delete Task ---")

    task_id = get_task_id()
    if task_id is None:
        return

    if service.delete_task(task_id):
        print("[OK] Task deleted successfully!")
    else:
        print("Error: Task not found.")


def handle_exit(service: TaskService) -> None:
    """Handle the Exit menu option.

    Displays a warning about data loss and exits the application.

    Args:
        service: The TaskService instance (used to check task count).

    Raises:
        SystemExit: Always raised to exit the application.

    Example:
        >>> service = TaskService()
        >>> handle_exit(service)
        [!] Note: All tasks will be lost (in-memory storage only).
        Goodbye! Thanks for using Todo App.
    """
    task_count = service.get_task_count()

    if task_count > 0:
        print(f"\n[!] Warning: You have {task_count} task(s) that will be lost.")

    print("[!] Note: All tasks will be lost (in-memory storage only).")
    print("\nGoodbye! Thanks for using Todo App.")
    raise SystemExit(0)
