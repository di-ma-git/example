from http import HTTPStatus

from requests import Session, Response
from common_api.base_api import BaseAPI


class ClientSignature(BaseAPI):
    _response: dict

    def __init__(self, session: Session):
        super().__init__(session)

    def signature(self) -> Response:
        response = self.post(
            "contract/fvno/signature"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        return response

    def next(self, view: str) -> Response:
        payload = {
            "data": {
                "code": "333333"
            },
            "from": view
        }
        response = self.post(
            "contract/fvno/signature/next",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return response
