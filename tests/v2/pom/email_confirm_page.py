from http import HTTPStatus

from tests.v2.pom.base_api import BaseAPI
from requests import Response, Session


class EmailConfirmPage(BaseAPI):
    _response: Response

    def __init__(self, session: Session):
        super().__init__(session)

    def get_email(self) -> Response:
        self._response = self.get(
            "contract",
            {"fields[]": "email"}
        )
        assert self._response.status_code == HTTPStatus.OK
        assert self._response.json().get("contents")
        return self._response

    def confirm_email(self) -> Response:
        response = self.post(
            "contract/fvno/email-confirm"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        return response

    def next(self, code: str, view: str) -> Response:
        payload = {
            "data": {
                "code": code,
                "email": self._response.json().get("contents", {}).get("email", {}).get("value")
            },
            "view": view
        }
        response = self.post(
            "contract/fvno/email-confirm/next",
            payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return response
