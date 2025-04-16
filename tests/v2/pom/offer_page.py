from http import HTTPStatus

from tests.v2.pom.base_api import BaseAPI
from requests import Response, Session


class OfferPage(BaseAPI):

    def __init__(self, session: Session):
        super().__init__(session)

    def settings(self) -> Response:
        response = self.get(
            "contract/settings",
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents", {}).get("success") == True
        return response

    def next(self, view: str) -> Response:
        payload = {"from": view}
        response = self.post(
            "contract/fvno/offer/next",
            payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return response
