from typing import Any, Optional

from pydantic import BaseModel

from routine.api.client import RoutineClient
from routine.util import _create_id, _get_now_as_str


class EtagDTO(BaseModel):
    time: str
    version: int


class ScheduledDayDTO(list[int]):
    pass


class ScheduledWeekDTO(BaseModel):
    n: int
    year: int


class IntegrationDataDTO(BaseModel):
    page: str
    type: str
    database: str


class BlockDTO(BaseModel):
    id: str
    type: str
    checked: bool
    content: str
    task: str


class NotesDTO(BaseModel):
    blocks: list[BlockDTO]


class TaskDTO(BaseModel):
    title: str
    id: str
    created: str
    etag: EtagDTO
    scheduled: None | ScheduledWeekDTO | ScheduledDayDTO = None
    completed: Optional[str] = None
    starred: Optional[bool] = None
    ignored: Optional[str] = None
    integration_id: Optional[str] = None
    integration_data: Optional[IntegrationDataDTO] = None
    distant_task_id: Optional[str] = None
    url: Optional[str] = None
    allocations: Optional[list[str]] = None
    notes: Optional[NotesDTO] = None


class Task:
    """A Routine task.

    Getters/setters for properties are delegated to DTOs.
    """

    def __init__(self, title) -> None:
        now_str = _get_now_as_str()
        self._dto = TaskDTO(
            title=title,
            id=_create_id(),
            created=now_str,
            etag=EtagDTO(time=now_str, version=0),
        )

    def __getattr__(self, name: str) -> Any:
        if name in self._dto.__fields__:
            return self._dto.__getattribute__(name)
        else:
            return self.__dict__[name]
        # if name in self._dto.__fields__:
        #     print(name)
        #     return self._dto.__getattribute__(name)
        # elif name in self.__dict__:
        #     print(name)
        #     return self.__dict__[name]
        # else:
        #     raise ValueError(f"Task objects does not have a field called {name!r}")

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ("id", "title", "starred"):
            self._dto = TaskDTO(**RoutineClient().tasks.update(self.id, {name: value}))
        elif name == "_dto":
            self.__dict__[name] = value
        else:
            print(self.__dict__)
            raise ValueError(f"Task objects does not have a field called {name!r}")

    @classmethod
    def from_json(cls, json_data: dict) -> "Task":
        new_task = cls.__new__(cls)
        new_task._dto = TaskDTO(**json_data)
        return new_task

    @staticmethod
    def from_id(task_id: str) -> "Task":
        return RoutineClient().tasks.get_by_id(task_id)

    def create(self) -> None:
        self.id = _create_id()
        RoutineClient().tasks.create(self.title, self.scheduled)

    def delete(self) -> None:
        RoutineClient().tasks.delete(self.id)
        print(f"Deleted task {self.title!r}")

    def __str__(self) -> str:
        return f"Task(id: {self.id!r}, title: {self.title!r}, scheduled: {self.scheduled})"

    def __repr__(self) -> str:
        return str(self)
