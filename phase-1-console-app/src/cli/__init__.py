"""Command-line interface components for the Todo application."""

from src.cli.handlers import (
    get_user_input,
    handle_add_task,
    handle_view_tasks,
    handle_mark_complete,
    handle_update_task,
    handle_delete_task,
    handle_exit,
)
from src.cli.menu import display_menu

__all__ = [
    "display_menu",
    "get_user_input",
    "handle_add_task",
    "handle_view_tasks",
    "handle_mark_complete",
    "handle_update_task",
    "handle_delete_task",
    "handle_exit",
]
