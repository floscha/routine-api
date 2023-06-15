from routine.api.client import RoutineClient
from routine.model import Page, Task
from routine.version import __version__

__all__ = ["__version__", "Page", "Task"]


def get_all_tasks():
    return RoutineClient().tasks.get_all()


def get_inbox_tasks():
    return RoutineClient().tasks.get_inbox()


def get_all_pages():
    return RoutineClient().pages.get_all()
