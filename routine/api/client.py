from os import environ
from typing import Final, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL: Final[str] = "https://api.routine.co"


class HttpMethod:
    GET: Final[str] = "get"
    POST: Final[str] = "post"
    PUT: Final[str] = "put"
    PATCH: Final[str] = "patch"
    DELETE: Final[str] = "delete"


class RoutineClient:
    _instance = None

    def __new__(cls) -> "RoutineClient":
        if cls._instance is None:
            cls._instance = super(RoutineClient, cls).__new__(cls)
            cls._auth_token = environ["ROUTINE_TOKEN"]
            cls._bearer_token = None

            from routine.api import PagesEndpoint, TasksEndpoint

            cls.tasks = TasksEndpoint(cls._instance)
            cls.pages = PagesEndpoint(cls._instance)
        return cls._instance

    def _renew_token(self):
        print("Renewing bearer token...")
        headers = {
            "Authorization": f"Basic {self._auth_token}",
            "x-routine-version": "0.12.0",
        }
        r = requests.post(f"{BASE_URL}/oauth/renew", headers=headers)
        # print(r.status_code)
        # can fail with 401: {'reason': 'authentication token is insufficient: personal token required'}
        self._bearer_token = r.json()["token"]

    def _make_request(self, http_method: str, endpoint: str, payload: Optional[dict] = None):
        headers = {"authorization": f"Bearer {self._bearer_token}"}
        r = getattr(requests, http_method)(f"{BASE_URL}/{endpoint}", headers=headers, json=payload)
        json_data = r.json()

        # Can also be "authentication token is invalid: invalid cryptographic token"
        if r.status_code == 401:  # and json_data["reason"] == "authentication token is expired":
            self._renew_token()
            return self._make_request(http_method, endpoint)

        if r.status_code != 200:
            raise Exception(f"Error {r.status_code}: {json_data['reason']}")
        else:
            return json_data
