from http import HTTPStatus

from requests import Session, Response
from tests.v2.pom.base_api import BaseAPI


class EmployeeConfirmPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session):
        super().__init__(session)

    def get_client_document(self) -> Response:
        params = {
            "fields[]": [
                "attorney",
                "attorneyDocument",
                "documentPrimary",
                "documentSecondary",
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
        return response

    def employee_confirm(self) -> Response:
        response = self.get(
            "contract/fvno/employee-confirm"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        return response

    def next(self, code: str, view: str) -> Response:
        payload = {
            "data": {
                "code": code
            },
            "from": view
        }
        response = self.post(
            "contract/fvno/employee-confirm/next",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return response
