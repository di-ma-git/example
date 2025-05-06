from http import HTTPStatus
from requests import Response, Session
from common_api.base_api import BaseAPI
from context import TestContext
from database.task_repository import TaskRepository


class LoginPage(BaseAPI):

    def __init__(self, session: Session, test_context: TestContext, task_repository: TaskRepository):
        super().__init__(session)
        self._test_context = test_context
        self._task_repository = task_repository

    def login(self) -> 'LoginPage':
        params = {"phone": self._test_context.get_param("identification_value")}
        response = self.get("login", params)
        assert response.status_code == HTTPStatus.OK

        # TODO для конутра TEST достать код (password) для запроса из базы

        payload = {"password": "111111", "phone": self._test_context.get_param("identification_value")}
        response = self.post("login", payload)
        assert response.status_code == HTTPStatus.OK
        token = response.json().get("contents", {}).get("token")
        assert token

        self.session.headers.update({"Authorization": f"Bearer {token}"})

        return self

    def find_task(self) -> 'LoginPage':
        response = self.get("task")
        assert response.status_code == HTTPStatus.OK
        task_id_from_token = response.json()["contents"]["tasks"][0]["taskId"]
        assert task_id_from_token == self._test_context.get_param("task_id")

        payload = {"taskId": task_id_from_token}
        response = self.post("task", payload)
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"

        return self
