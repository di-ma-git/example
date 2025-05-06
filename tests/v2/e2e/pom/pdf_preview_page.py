from http import HTTPStatus

from requests import Session, Response
from common_api.base_api import BaseAPI
from context import TestContext


class PdfPreviewPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session, test_context: TestContext):
        super().__init__(session)
        self._test_context = test_context

    def get_files(self) -> 'PdfPreviewPage':
        params = {
            "fields[]": [
                "files"
            ]
        }
        response = self.get(
            "contract",
            params=params
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        # TODO добавить проверку ссылок из UPLOAD
        return self

    def next(self) -> 'PdfPreviewPage':
        payload = {"from": self._test_context.get_param("current_view")}
        response = self.post(
            "contract/fvno/pdf-preview/next",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return self
