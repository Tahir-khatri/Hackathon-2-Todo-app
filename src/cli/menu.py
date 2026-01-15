"""Menu display for the Todo application.

This module provides the main menu display function that shows
all available operations to the user.
"""


def display_menu() -> None:
    """Display the main menu with all available options.

    Shows a formatted menu with numbered options for all todo operations:
    1. Add Task
    2. View All Tasks
    3. Mark Task Complete
    4. Update Task
    5. Delete Task
    6. Exit

    Example:
        >>> display_menu()
        ========== Todo App ==========
        1. Add Task
        2. View All Tasks
        3. Mark Task Complete
        4. Update Task
        5. Delete Task
        6. Exit
        ==============================
    """
    print("\n========== Todo App ==========")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Mark Task Complete")
    print("4. Update Task")
    print("5. Delete Task")
    print("6. Exit")
    print("==============================")
