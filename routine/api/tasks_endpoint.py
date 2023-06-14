from typing import TYPE_CHECKING

from routine.api.client import HttpMethod, RoutineClient

if TYPE_CHECKING:
    from routine.model.task import Task
from routine.util import _create_id, _get_now_as_str


class TasksEndpoint:
    def __init__(self, client: RoutineClient):
        self._client = client

    def get_all(self) -> list["Task"]:
        from routine.model import Task

        return [Task.from_json(json_data) for json_data in self._client._make_request(HttpMethod.GET, "tasks")]

    def get_inbox(self) -> list["Task"]:
        from routine.model import Task

        return [
            Task.from_json(json_data)
            for json_data in self._client._make_request(HttpMethod.GET, "tasks")
            if not json_data.get("scheduled")
        ]

    def get_by_id(self, task_id: str) -> "Task":
        from routine.model import Task

        return Task.from_json(self._client._make_request(HttpMethod.GET, f"tasks/{task_id}"))

    def create(self, title: str, scheduled: list[int]):
        "Create a new task."
        task_id = _create_id()
        now = _get_now_as_str()
        payload = {
            "created": now,
            "etag": {"time": now, "version": 0},
            "id": f"{task_id}",
            "scheduled": scheduled,
            "title": title,
            "canEditTitle": True,  # Why would this be false?
        }
        return self._client._make_request(HttpMethod.PUT, f"tasks/{task_id}", payload=payload)

    def delete(self, task_id):
        self._client._make_request(HttpMethod.DELETE, f"tasks/{task_id}")

    def update(self, task_id: str, payload: dict):
        return self._client._make_request(HttpMethod.PATCH, f"tasks/{task_id}", payload=payload)

    def complete(self, task_id: str):
        return self.update(task_id, {"completed": _get_now_as_str()})

    def uncomplete(self, task_id: str):
        return self.update(task_id, {"completed": None})
