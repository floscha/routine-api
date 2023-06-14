from typing import TYPE_CHECKING

from routine.api.client import HttpMethod, RoutineClient

if TYPE_CHECKING:
    from routine.model import Page


class PagesEndpoint:
    def __init__(self, client: RoutineClient):
        self._client = client

    def get_all(self) -> list["Page"]:
        from routine.model import Page

        return [Page(**json_data) for json_data in self._client._make_request(HttpMethod.GET, "pages")]
