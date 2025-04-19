from http import HTTPStatus

from common_api.base_api import BaseAPI
from requests import Response, Session


class EmailConfirmPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session):
        super().__init__(session)

    def get_email(self) -> Response:
        response = self.get(
            "contract",
            {"fields[]": "email"}
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        self._response = response.json()
        return response

    def confirm_email(self) -> Response:
        response = self.post(
            "contract/fvno/email-confirm"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        return response

    def next(self, code: str, view: str) -> Response:
        contents = self._response.get("contents", {})
        payload = {
            "data": {
                "code": code,
                "email": contents.get("email", {}).get("value")
            },
            "from": view
        }
        response = self.post(
            "contract/fvno/email-confirm/next",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return response
