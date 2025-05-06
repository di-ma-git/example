from http import HTTPStatus

from requests import Session, Response
from common_api.base_api import BaseAPI
from context import TestContext


class EmployeeConfirmPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session, test_context: TestContext):
        super().__init__(session)
        self._test_context = test_context

    def get_client_document(self) -> 'EmployeeConfirmPage':
        params = {
            "fields[]": [
                "middleName",
                "name",
                "surname"
            ]
        }
        response = self.get(
            "contract",
            params=params
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        return self

    def employee_confirm(self) -> 'EmployeeConfirmPage':
        response = self.get(
            "contract/fvno/employee-confirm"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        return self

    def next(self) -> 'EmployeeConfirmPage':
        payload = {
            "data": {
                "code": self._test_context.get_param("installer_code")
            },
            "from": self._test_context.get_param("current_view")
        }
        response = self.post(
            "contract/fvno/employee-confirm/next",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return self
