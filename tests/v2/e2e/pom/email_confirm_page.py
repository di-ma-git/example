import time
from http import HTTPStatus

from common_api.base_api import BaseAPI
from requests import Response, Session

from common_api.camunda_api import CamundaAPI
from context import TestContext
from database.task_repository import TaskRepository


class EmailConfirmPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session, test_context: TestContext, task_repository: TaskRepository):
        super().__init__(session)
        self._test_context = test_context
        self._task_repository = task_repository

    def get_email(self) -> 'EmailConfirmPage':
        response = self.get(
            "contract",
            {"fields[]": "email"}
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        self._response = response.json()
        return self

    def confirm_email(self) -> 'EmailConfirmPage':
        response = self.post(
            "contract/fvno/email-confirm"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")

        assert CamundaAPI.get_activity_by_instance_id(self._test_context.get_param("instance_id")) == "Gateway_0y7jdjo"

        return self

    def next(self) -> 'EmailConfirmPage':
        time.sleep(2)
        code = self._task_repository.get_confirm_email_code_by_task_id(self._test_context.get_param("task_id"))

        contents = self._response.get("contents", {})
        payload = {
            "data": {
                "code": code,
                "email": contents.get("email", {}).get("value")
            },
            "from": self._test_context.get_param("current_view")
        }
        response = self.post(
            "contract/fvno/email-confirm/next",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return self
