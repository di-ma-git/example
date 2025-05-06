from http import HTTPStatus

from requests import Session, Response
from common_api.base_api import BaseAPI
from context import TestContext
from database.task_repository import TaskRepository


class ClientSignaturePage(BaseAPI):
    _response: dict

    def __init__(self, session: Session, test_context: TestContext, task_repository: TaskRepository):
        super().__init__(session)
        self._test_context = test_context
        self._task_repository = task_repository

    def signature(self) -> 'ClientSignaturePage':
        response = self.post(
            "contract/fvno/signature"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        return self

    def next(self) -> 'ClientSignaturePage':
        # TODO для конутра TEST достать код (code) для запроса из базы

        payload = {
            "data": {
                "code": "333333"
            },
            "from": self._test_context.get_param("current_view")
        }
        response = self.post(
            "contract/fvno/signature/next",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return self
