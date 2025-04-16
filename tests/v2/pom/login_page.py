from http import HTTPStatus
from requests import Response, Session
from tests.v2.pom.base_api import BaseAPI


class LoginPage(BaseAPI):

    def __init__(self, session: Session):
        super().__init__(session)

    def login(self, code: str, phone: str) -> Response:
        params = {"phone": phone}
        response = self.get("login", params)
        payload = {"password": code, "phone": phone}
        assert response.status_code == HTTPStatus.OK

        response = self.post("login", payload)
        assert response.status_code == HTTPStatus.OK
        token = response.json().get("contents", {}).get("token")
        assert token

        self.session.headers.update({"Authorization": f"Bearer {token}"})

        return response

    def find_task(self, task_id) -> Response:
        response = self.get("task")
        assert response.status_code == HTTPStatus.OK
        task_id_from_token = response.json()["contents"]["tasks"][0]["taskId"]
        assert task_id_from_token == task_id

        payload = {"taskId": task_id_from_token}
        response = self.post("task", payload)
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"

        return response
