"""Main entry point for the Todo Console Application.

This module contains the main function and application loop that
drives the CLI todo application.
"""

from src.cli.handlers import (
    get_user_input,
    handle_add_task,
    handle_delete_task,
    handle_exit,
    handle_mark_complete,
    handle_update_task,
    handle_view_tasks,
)
from src.cli.menu import display_menu
from src.services.task_service import TaskService


def main() -> None:
    """Run the Todo Console Application.

    This is the main entry point that initializes the task service
    and runs the main application loop. The loop displays a menu,
    gets user input, and dispatches to the appropriate handler.

    The application exits when the user selects option 6 (Exit)
    or presses Ctrl+C.

    Example:
        >>> main()  # Starts the interactive application
    """
    print("Welcome to Todo App!")
    print("A simple in-memory task manager.")

    service = TaskService()

    # Map menu options to handlers
    handlers = {
        "1": handle_add_task,
        "2": handle_view_tasks,
        "3": handle_mark_complete,
        "4": handle_update_task,
        "5": handle_delete_task,
        "6": handle_exit,
    }

    while True:
        try:
            display_menu()
            choice = get_user_input("Enter your choice: ")

            if choice in handlers:
                handlers[choice](service)
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

        except KeyboardInterrupt:
            print("\n\nGoodbye! (interrupted)")
            break
        except SystemExit:
            break


if __name__ == "__main__":
    main()
