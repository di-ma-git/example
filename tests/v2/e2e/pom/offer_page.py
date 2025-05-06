from http import HTTPStatus

from common_api.base_api import BaseAPI
from requests import Response, Session
from context import TestContext


class OfferPage(BaseAPI):

    def __init__(self, session: Session, test_context: TestContext):
        super().__init__(session)
        self._test_context = test_context

    def settings(self) -> 'OfferPage':
        response = self.get(
            "contract/settings",
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents", {}).get("success") is True
        return self

    def next(self) -> 'OfferPage':
        payload = {"from": self._test_context.get_param("current_view")}
        response = self.post(
            "contract/fvno/offer/next",
            payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return self
